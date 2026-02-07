"""
AI Agent - Autonomous Client Analysis and Email Generation
Uses Google Gemini for intelligent analysis and personalized outreach
"""
import os
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import google.generativeai as genai
from dotenv import load_dotenv
from rag_system import RAGSystem

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


class JarvisAgent:
    def __init__(self):
        """Initialize the Jarvis AI Agent."""
        self.model = genai.GenerativeModel('gemini-pro')
        self.rag = RAGSystem()
        self.data_dir = Path(__file__).parent.parent / "data"
        
    def load_clients(self) -> List[Dict[str, Any]]:
        """Load client context data."""
        client_file = self.data_dir / "client_context.json"
        try:
            with open(client_file, 'r') as f:
                return json.load(f)
        except:
            return []
    
    def analyze_client_opportunity(self, client: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a single client for opportunities using RAG + Gemini."""
        
        # Search RAG for relevant context
        search_query = f"{client['name']} {client['company']} {' '.join(client.get('pain_points', []))}"
        rag_results = self.rag.search(search_query, n_results=3)
        
        # Build context for Gemini
        rag_context = "\n".join([r['content'] for r in rag_results]) if rag_results else "No additional context available."
        
        prompt = f"""You are Jarvis, an AI financial advisor assistant. Analyze this client for proactive outreach opportunities.

CLIENT PROFILE:
Name: {client['name']}
Company: {client['company']}
Industry: {client['industry']}
Revenue: {client.get('revenue_range', 'Unknown')}
Company Size: {client.get('company_size', 'Unknown')}

KEY INSIGHTS:
{chr(10).join(['- ' + insight for insight in client.get('key_insights', [])])}

PAIN POINTS:
{chr(10).join(['- ' + pain for pain in client.get('pain_points', [])])}

ADDITIONAL CONTEXT FROM DOCUMENTS:
{rag_context[:1000]}

TASK:
1. Identify the MOST COMPELLING opportunity for proactive outreach
2. Rate the priority (1-10, where 10 is urgent/high-value)
3. Suggest the best approach angle
4. Explain why NOW is the right time to reach out

Respond in JSON format:
{{
    "opportunity_type": "brief category (e.g., 'Tax Planning', 'R&D Credits', 'Exit Strategy')",
    "priority_score": 8,
    "timing_reason": "why reach out now",
    "approach_angle": "the hook/value proposition",
    "estimated_value": "potential $ impact or benefit"
}}"""

        try:
            response = self.model.generate_content(prompt)
            # Extract JSON from response
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            analysis = json.loads(response_text)
            analysis['client_id'] = client['client_id']
            analysis['client_name'] = client['name']
            return analysis
            
        except Exception as e:
            print(f"Error analyzing {client['name']}: {e}")
            # Return default analysis
            return {
                "client_id": client['client_id'],
                "client_name": client['name'],
                "opportunity_type": client.get('pain_points', ['General Advisory'])[0] if client.get('pain_points') else 'General Advisory',
                "priority_score": client.get('engagement_score', 50) // 10,
                "timing_reason": "Regular check-in based on client profile",
                "approach_angle": "Proactive advisory support",
                "estimated_value": "Ongoing relationship value"
            }
    
    def generate_email(self, client: Dict[str, Any], opportunity: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a personalized email using Gemini."""
        
        prompt = f"""You are Jarvis, writing an email on behalf of a financial advisor. Create a warm, personalized outreach email.

CLIENT: {client['name']}
COMPANY: {client['company']}
INDUSTRY: {client['industry']}

OPPORTUNITY: {opportunity['opportunity_type']}
WHY NOW: {opportunity['timing_reason']}
VALUE PROPOSITION: {opportunity['approach_angle']}
ESTIMATED IMPACT: {opportunity['estimated_value']}

KEY INSIGHTS ABOUT CLIENT:
{chr(10).join(['- ' + insight for insight in client.get('key_insights', [])[:3]])}

WRITING GUIDELINES:
- Warm and personal (not salesy)
- Show you've done research (reference specific insights)
- Clear value proposition
- Soft call-to-action (suggest a brief call)
- Professional but friendly tone
- Keep it concise (150-200 words)
- Subject line should be compelling and specific

Respond in JSON format:
{{
    "subject": "email subject line",
    "body": "full email body",
    "tone": "professional/friendly/consultative"
}}"""

        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            email_data = json.loads(response_text)
            
            # Create full email record
            email_id = f"email_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{client['client_id']}"
            
            return {
                "id": email_id,
                "client_id": client['client_id'],
                "client_name": client['name'],
                "client_email": client['email'],
                "subject": email_data['subject'],
                "body": email_data['body'],
                "preview": email_data['body'][:150] + "...",
                "full_content": email_data['body'],
                "sent_date": datetime.now().isoformat(),
                "status": "sent",
                "opportunity_type": opportunity['opportunity_type'],
                "priority_score": opportunity['priority_score']
            }
            
        except Exception as e:
            print(f"Error generating email for {client['name']}: {e}")
            # Return default email
            return {
                "id": f"email_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{client['client_id']}",
                "client_id": client['client_id'],
                "client_name": client['name'],
                "client_email": client['email'],
                "subject": f"Quick check-in - {opportunity['opportunity_type']}",
                "body": f"Hi {client['name']},\n\nI wanted to reach out regarding {opportunity['opportunity_type']}. Based on your recent activities, I think there might be some valuable opportunities we should discuss.\n\nWould you have time for a brief call this week?\n\nBest regards,\nYour Financial Advisor",
                "preview": f"Hi {client['name']}, I wanted to reach out regarding {opportunity['opportunity_type']}...",
                "full_content": f"Hi {client['name']},\n\nI wanted to reach out regarding {opportunity['opportunity_type']}. Based on your recent activities, I think there might be some valuable opportunities we should discuss.\n\nWould you have time for a brief call this week?\n\nBest regards,\nYour Financial Advisor",
                "sent_date": datetime.now().isoformat(),
                "status": "sent",
                "opportunity_type": opportunity['opportunity_type'],
                "priority_score": opportunity['priority_score']
            }
    
    def overnight_analysis_run(self, top_n: int = 8) -> Dict[str, Any]:
        """
        Simulate the overnight analysis run.
        Analyzes all clients, identifies top opportunities, generates emails.
        """
        print("\n🌙 Starting Overnight Analysis Run...")
        print("=" * 60)
        
        # Load all clients
        clients = self.load_clients()
        print(f"📊 Analyzing {len(clients)} clients...")
        
        # Analyze each client
        opportunities = []
        for i, client in enumerate(clients, 1):
            print(f"\n[{i}/{len(clients)}] Analyzing {client['name']}...")
            opportunity = self.analyze_client_opportunity(client)
            opportunities.append({
                "client": client,
                "opportunity": opportunity
            })
            print(f"   ✓ Priority Score: {opportunity['priority_score']}/10")
            print(f"   ✓ Opportunity: {opportunity['opportunity_type']}")
        
        # Sort by priority score
        opportunities.sort(key=lambda x: x['opportunity']['priority_score'], reverse=True)
        
        # Take top N
        top_opportunities = opportunities[:top_n]
        
        print(f"\n🎯 Top {top_n} Opportunities Identified")
        print("=" * 60)
        
        # Generate emails for top opportunities
        emails_generated = []
        for i, opp in enumerate(top_opportunities, 1):
            client = opp['client']
            opportunity = opp['opportunity']
            
            print(f"\n[{i}/{top_n}] Generating email for {client['name']}...")
            email = self.generate_email(client, opportunity)
            emails_generated.append(email)
            print(f"   ✓ Subject: {email['subject']}")
        
        # Save generated emails
        emails_file = self.data_dir / "emails_sent.json"
        with open(emails_file, 'w') as f:
            json.dump(emails_generated, f, indent=2)
        
        print(f"\n✅ Overnight Run Complete!")
        print(f"   📧 {len(emails_generated)} emails generated and 'sent'")
        print(f"   💾 Saved to {emails_file}")
        
        return {
            "total_clients_analyzed": len(clients),
            "opportunities_identified": len(opportunities),
            "emails_sent": len(emails_generated),
            "top_opportunities": [
                {
                    "client": opp['client']['name'],
                    "opportunity": opp['opportunity']['opportunity_type'],
                    "priority": opp['opportunity']['priority_score']
                }
                for opp in top_opportunities
            ]
        }


def run_overnight_analysis():
    """Standalone function to run the overnight analysis."""
    agent = JarvisAgent()
    return agent.overnight_analysis_run(top_n=8)


if __name__ == "__main__":
    # Run the overnight analysis
    results = run_overnight_analysis()
    
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"Total Clients Analyzed: {results['total_clients_analyzed']}")
    print(f"Emails Sent: {results['emails_sent']}")
    print("\nTop Opportunities:")
    for opp in results['top_opportunities']:
        print(f"  • {opp['client']}: {opp['opportunity']} (Priority: {opp['priority']}/10)")
