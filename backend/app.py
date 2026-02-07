from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import sys

# Add backend to path for imports
sys.path.append(str(Path(__file__).parent))

app = FastAPI(title="Jarvis Auto-Pilot Agent API", version="2.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data file paths
DATA_DIR = Path(__file__).parent / "data"
EMAILS_FILE = DATA_DIR / "emails_sent.json"
RESPONSES_FILE = DATA_DIR / "responses.json"
CLIENT_CONTEXT_FILE = DATA_DIR / "client_context.json"
DOCUMENTS_DIR = DATA_DIR / "client_documents"


def load_json_file(file_path: Path) -> List[Dict[str, Any]]:
    """Load and parse a JSON file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Jarvis Auto-Pilot Agent API",
        "version": "2.0.0",
        "status": "operational",
        "tagline": "AI that acts FOR you, not just advises",
        "endpoints": {
            "dashboard": "/api/dashboard",
            "emails": "/api/emails",
            "responses": "/api/responses",
            "clients": "/api/clients",
            "stats": "/api/stats",
            "activity": "/api/activity",
            "warm_leads": "/api/warm-leads",
            "run_analysis": "/api/run-analysis",
            "ingest_documents": "/api/ingest-documents",
            "rag_stats": "/api/rag-stats"
        }
    }


@app.get("/api/dashboard")
async def get_dashboard():
    """Get complete dashboard data - the main view for advisors."""
    emails = load_json_file(EMAILS_FILE)
    responses = load_json_file(RESPONSES_FILE)
    clients = load_json_file(CLIENT_CONTEXT_FILE)
    
    # Calculate metrics
    total_emails = len(emails)
    total_responses = len(responses)
    response_rate = (total_responses / total_emails * 100) if total_emails > 0 else 0
    
    # Warm leads (responses with high interest)
    warm_leads = []
    for response in responses:
        # Find corresponding email (by ID first, then fallback to email)
        email = next((e for e in emails if e["id"] == response["email_id"]), None)
        if not email:
            email = next((e for e in emails if e["client_email"] == response["client_email"]), None)
            
        client = next((c for c in clients if c["email"] == response["client_email"]), None)
        
        if email and client:
            warm_leads.append({
                "id": response["id"],
                "client_name": response["client_name"],
                "client_email": response["client_email"],
                "company": client.get("company", ""),
                "industry": client.get("industry", ""),
                "email_subject": email.get("subject", ""),
                "email_sent": email.get("sent_date", ""),
                "response_received": response.get("response_date", ""),
                "response_text": response.get("response_text", ""),
                "sentiment": response.get("sentiment", "neutral"),
                "interest_level": response.get("interest_level", "medium"),
                "priority": response.get("priority", "medium"),
                "next_action": response.get("next_action", "Follow up"),
                "engagement_score": client.get("engagement_score", 0),
                "email_body": email.get("full_content") or email.get("body", ""),
                "context": {
                    "key_insights": client.get("key_insights", []),
                    "pain_points": client.get("pain_points", [])
                }
            })
    
    # Sort warm leads by priority and interest
    priority_order = {"high": 3, "medium": 2, "low": 1}
    warm_leads.sort(key=lambda x: (
        priority_order.get(x["priority"], 0),
        x["engagement_score"]
    ), reverse=True)
    
    # Recent activity
    recent_activity = []
    for email in emails[-10:]:  # Last 10 emails
        recent_activity.append({
            "type": "email_sent",
            "timestamp": email.get("sent_date", ""),
            "description": f"Sent email to {email.get('client_name', 'Unknown')}",
            "client": email.get("client_name", ""),
            "subject": email.get("subject", ""),
            "id": email.get("id"),
            "full_content": email.get("full_content") or email.get("body", "")
        })
    
    for response in responses:
        recent_activity.append({
            "type": "response_received",
            "timestamp": response.get("response_date", ""),
            "description": f"Response from {response.get('client_name', 'Unknown')}",
            "client": response.get("client_name", ""),
            "sentiment": response.get("sentiment", "neutral"),
            "response_text": response.get("response_text", ""),
            "id": response.get("id")
        })
    
    # Sort by timestamp
    recent_activity.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

    # Determine last analyzed time (latest email sent)
    last_analyzed = emails[-1]["sent_date"] if emails else None
    
    return JSONResponse(content={
        "success": True,
        "data": {
            "metrics": {
                "emails_sent_today": total_emails,
                "responses_received": total_responses,
                "response_rate": response_rate,
                "warm_leads_count": len(warm_leads),
                "total_clients": len(clients)
            },
            "last_analyzed": last_analyzed,
            "warm_leads": warm_leads[:10],  # Top 10
            "recent_activity": recent_activity[:15],  # Last 15 activities
            "top_opportunities": emails[:10]  # Top N opportunities from analysis
        }
    })


@app.get("/api/warm-leads")
async def get_warm_leads():
    """Get all warm leads with full context."""
    emails = load_json_file(EMAILS_FILE)
    responses = load_json_file(RESPONSES_FILE)
    clients = load_json_file(CLIENT_CONTEXT_FILE)
    
    warm_leads = []
    for response in responses:
        email = next((e for e in emails if e["id"] == response["email_id"]), None)
        client = next((c for c in clients if c["email"] == response["client_email"]), None)
        
        if email and client:
            warm_leads.append({
                "id": response["id"],
                "client": {
                    "name": client["name"],
                    "email": client["email"],
                    "company": client.get("company", ""),
                    "industry": client.get("industry", ""),
                    "engagement_score": client.get("engagement_score", 0)
                },
                "jarvis_action": {
                    "email_sent": email.get("sent_date", ""),
                    "subject": email.get("subject", ""),
                    "body": email.get("full_content", "")
                },
                "client_response": {
                    "received": response.get("response_date", ""),
                    "text": response.get("response_text", ""),
                    "sentiment": response.get("sentiment", "neutral"),
                    "interest_level": response.get("interest_level", "medium")
                },
                "suggested_action": response.get("next_action", "Follow up"),
                "priority": response.get("priority", "medium"),
                "context_for_call": {
                    "key_insights": client.get("key_insights", []),
                    "pain_points": client.get("pain_points", []),
                    "last_interaction": email.get("sent_date", "")
                }
            })
    
    return JSONResponse(content={"success": True, "data": warm_leads})


@app.get("/api/emails")
async def get_emails():
    """Get all sent emails."""
    emails = load_json_file(EMAILS_FILE)
    return JSONResponse(content={"success": True, "data": emails, "count": len(emails)})


@app.get("/api/responses")
async def get_responses():
    """Get all client responses."""
    responses = load_json_file(RESPONSES_FILE)
    return JSONResponse(content={"success": True, "data": responses, "count": len(responses)})


@app.get("/api/clients")
async def get_clients():
    """Get all client context data."""
    clients = load_json_file(CLIENT_CONTEXT_FILE)
    return JSONResponse(content={"success": True, "data": clients, "count": len(clients)})


@app.get("/api/stats")
async def get_stats():
    """Get dashboard statistics."""
    emails = load_json_file(EMAILS_FILE)
    responses = load_json_file(RESPONSES_FILE)
    clients = load_json_file(CLIENT_CONTEXT_FILE)
    
    total_emails = len(emails)
    total_responses = len(responses)
    response_rate = (total_responses / total_emails * 100) if total_emails > 0 else 0
    
    engagement_scores = [c.get("engagement_score", 0) for c in clients]
    avg_engagement = sum(engagement_scores) / len(engagement_scores) if engagement_scores else 0
    
    high_priority = sum(1 for r in responses if r.get("priority") == "high")
    
    sentiment_counts = {"positive": 0, "neutral": 0, "negative": 0}
    for response in responses:
        sentiment = response.get("sentiment", "neutral")
        sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1
    
    return JSONResponse(content={
        "success": True,
        "data": {
            "total_emails_sent": total_emails,
            "total_responses": total_responses,
            "response_rate": round(response_rate, 1),
            "high_priority_leads": high_priority,
            "avg_engagement_score": round(avg_engagement, 1),
            "total_clients": len(clients),
            "sentiment_distribution": sentiment_counts
        }
    })


@app.get("/api/activity")
async def get_activity():
    """Get recent activity timeline."""
    emails = load_json_file(EMAILS_FILE)
    responses = load_json_file(RESPONSES_FILE)
    
    activity = []
    
    for email in emails:
        activity.append({
            "type": "email_sent",
            "timestamp": email.get("sent_date"),
            "description": f"Email sent to {email.get('client_name')}",
            "subject": email.get("subject"),
            "client": email.get("client_name"),
            "id": email.get("id")
        })
    
    for response in responses:
        activity.append({
            "type": "response_received",
            "timestamp": response.get("response_date"),
            "description": f"Response from {response.get('client_name')}",
            "sentiment": response.get("sentiment"),
            "priority": response.get("priority"),
            "client": response.get("client_name"),
            "id": response.get("id")
        })
    
    activity.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    
    return JSONResponse(content={"success": True, "data": activity, "count": len(activity)})


@app.post("/api/run-analysis")
async def run_analysis(background_tasks: BackgroundTasks):
    """Trigger the overnight analysis run (using Multi-Agent System)."""
    try:
        # Import the new Agentic System
        from agentic_system import run_overnight_analysis
        
        # Run in background
        background_tasks.add_task(run_overnight_analysis)
        
        return JSONResponse(content={
            "success": True,
            "message": "Multi-Agent Analysis started in background. Agents: Research → Analysis → Email Writer.",
            "status": "running",
            "framework": "LangGraph"
        })
    except Exception as e:
        return JSONResponse(content={
            "success": False,
            "error": str(e)
        }, status_code=500)


@app.post("/api/ingest-documents")
async def ingest_documents():
    """Ingest client documents into RAG system."""
    try:
        from rag_system import ingest_documents
        
        results = ingest_documents(str(DOCUMENTS_DIR))
        
        return JSONResponse(content={
            "success": True,
            "message": "Documents ingested successfully",
            "results": results
        })
    except Exception as e:
        return JSONResponse(content={
            "success": False,
            "error": str(e)
        }, status_code=500)


@app.get("/api/rag-stats")
async def get_rag_stats():
    """Get RAG system statistics."""
    try:
        from rag_system import RAGSystem
        
        rag = RAGSystem()
        stats = rag.get_stats()
        
        return JSONResponse(content={
            "success": True,
            "data": stats
        })
    except Exception as e:
        return JSONResponse(content={
            "success": False,
            "error": str(e),
            "data": {"total_chunks": 0, "total_documents": 0, "sources": []}
        })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
