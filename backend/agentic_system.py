# """
# Agentic AI System using LangGraph
# Multi-agent workflow for autonomous client analysis and outreach
# """
# import os
# import json
# from pathlib import Path
# from typing import List, Dict, Any, TypedDict, Annotated
# from datetime import datetime
# import operator

# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import PydanticOutputParser
# from pydantic import BaseModel, Field
# from langgraph.graph import StateGraph, END
# from rag_system import RAGSystem

# # Load environment variables
# load_dotenv()


# # ============================================================================
# # PYDANTIC MODELS FOR STRUCTURED OUTPUT
# # ============================================================================

# class OpportunityAnalysis(BaseModel):
#     """Structured output for opportunity analysis."""
#     client_id: str = Field(description="Client identifier")
#     client_name: str = Field(description="Client name")
#     opportunity_type: str = Field(description="Type of opportunity (e.g., 'Tax Planning', 'R&D Credits')")
#     priority_score: int = Field(description="Priority score from 1-10", ge=1, le=10)
#     timing_reason: str = Field(description="Why reach out now")
#     approach_angle: str = Field(description="The hook/value proposition")
#     estimated_value: str = Field(description="Potential $ impact or benefit")
#     key_insights: List[str] = Field(description="Key insights about the client")


# class EmailContent(BaseModel):
#     """Structured output for email generation."""
#     subject: str = Field(description="Email subject line")
#     body: str = Field(description="Full email body")
#     tone: str = Field(description="Tone of the email (professional/friendly/consultative)")
#     personalization_elements: List[str] = Field(description="Specific personalization elements used")


# # ============================================================================
# # AGENT STATE
# # ============================================================================

# class AgentState(TypedDict):
#     """State passed between agents in the workflow."""
#     client: Dict[str, Any]
#     rag_context: str
#     opportunity_analysis: OpportunityAnalysis | None
#     email_content: EmailContent | None
#     errors: Annotated[List[str], operator.add]


# # ============================================================================
# # INDIVIDUAL AGENTS
# # ============================================================================

# class ResearchAgent:
#     """Agent responsible for gathering context from RAG system."""
    
#     def __init__(self, rag_system: RAGSystem):
#         self.rag = rag_system
    
#     def execute(self, state: AgentState) -> AgentState:
#         """Research client using RAG system."""
#         client = state["client"]
        
#         try:
#             # Build search query
#             search_query = f"{client['name']} {client['company']} {' '.join(client.get('pain_points', []))}"
            
#             # Search RAG
#             rag_results = self.rag.search(search_query, n_results=5)
            
#             # Combine context
#             context = "\n\n".join([
#                 f"Document: {r['metadata'].get('source', 'Unknown')}\n{r['content']}"
#                 for r in rag_results
#             ]) if rag_results else "No additional context available."
            
#             state["rag_context"] = context[:2000]  # Limit context size
#             print(f"✓ Research Agent: Gathered context for {client['name']}")
            
#         except Exception as e:
#             state["errors"].append(f"Research Agent error: {str(e)}")
#             state["rag_context"] = "No context available."
        
#         return state

# class AnalysisAgent:
#     """Agent responsible for analyzing opportunities."""
    
#     def __init__(self, llm: ChatGoogleGenerativeAI):
#         self.llm = llm
#         self.parser = PydanticOutputParser(pydantic_object=OpportunityAnalysis)
    
#     def execute(self, state: AgentState) -> AgentState:
#         """Analyze client for opportunities."""
#         client = state["client"]
#         rag_context = state["rag_context"]
        
#         try:
#             prompt = ChatPromptTemplate.from_messages([
#                 ("system", """You are an expert financial advisor AI analyzing clients for proactive outreach opportunities.
                
# Your task is to identify the MOST COMPELLING opportunity for this client based on:
# 1. Their current situation and recent activities
# 2. Pain points and challenges
# 3. Industry trends and timing
# 4. Potential financial impact

# {format_instructions}"""),
#                 ("user", """Analyze this client:

# CLIENT PROFILE:
# Name: {name}
# Company: {company}
# Industry: {industry}
# Revenue: {revenue}
# Company Size: {size}

# KEY INSIGHTS:
# {insights}

# PAIN POINTS:
# {pain_points}

# ADDITIONAL CONTEXT FROM DOCUMENTS:
# {rag_context}

# Identify the top opportunity and provide a structured analysis.""")
#             ])
            
#             chain = prompt | self.llm
            
#             response = chain.invoke({
#                 "format_instructions": self.parser.get_format_instructions(),
#                 "name": client['name'],
#                 "company": client.get('company', 'Unknown'),
#                 "industry": client.get('industry', 'Unknown'),
#                 "revenue": client.get('revenue_range', 'Unknown'),
#                 "size": client.get('company_size', 'Unknown'),
#                 "insights": '\n'.join(['- ' + i for i in client.get('key_insights', [])]),
#                 "pain_points": '\n'.join(['- ' + p for p in client.get('pain_points', [])]),
#                 "rag_context": rag_context
#             })
            
#             # Parse response
#             analysis_text = response.content
            
#             # Extract JSON from response
#             if "```json" in analysis_text:
#                 analysis_text = analysis_text.split("```json")[1].split("```")[0].strip()
#             elif "```" in analysis_text:
#                 analysis_text = analysis_text.split("```")[1].split("```")[0].strip()
            
#             analysis_dict = json.loads(analysis_text)
#             analysis_dict['client_id'] = client['client_id']
#             analysis_dict['client_name'] = client['name']
            
#             state["opportunity_analysis"] = OpportunityAnalysis(**analysis_dict)
#             print(f"✓ Analysis Agent: Identified {state['opportunity_analysis'].opportunity_type} for {client['name']}")
            
#         except Exception as e:
#             state["errors"].append(f"Analysis Agent error: {str(e)}")
#             # Fallback analysis
#             state["opportunity_analysis"] = OpportunityAnalysis(
#                 client_id=client['client_id'],
#                 client_name=client['name'],
#                 opportunity_type=client.get('pain_points', ['General Advisory'])[0] if client.get('pain_points') else 'General Advisory',
#                 priority_score=client.get('engagement_score', 50) // 10,
#                 timing_reason="Regular check-in based on client profile",
#                 approach_angle="Proactive advisory support",
#                 estimated_value="Ongoing relationship value",
#                 key_insights=client.get('key_insights', [])[:3]
#             )
        
#         return state


# class EmailWriterAgent:
#     """Agent responsible for writing personalized emails."""
    
#     def __init__(self, llm: ChatGoogleGenerativeAI):
#         self.llm = llm
#         self.parser = PydanticOutputParser(pydantic_object=EmailContent)
    
#     def execute(self, state: AgentState) -> AgentState:
#         """Generate personalized email."""
#         client = state["client"]
#         opportunity = state["opportunity_analysis"]
        
#         if not opportunity:
#             state["errors"].append("No opportunity analysis available")
#             return state
        
#         try:
#             prompt = ChatPromptTemplate.from_messages([
#                 ("system", """You are an expert email writer for financial advisors. Write warm, personalized outreach emails.

# GUIDELINES:
# - Warm and personal (not salesy)
# - Show you've done research (reference specific insights)
# - Clear value proposition
# - Soft call-to-action (suggest a brief call)
# - Professional but friendly tone
# - Concise (150-200 words)
# - Compelling subject line

# {format_instructions}"""),
#                 ("user", """Write an email for this client:

# CLIENT: {name}
# COMPANY: {company}
# INDUSTRY: {industry}

# OPPORTUNITY: {opportunity_type}
# WHY NOW: {timing_reason}
# VALUE PROPOSITION: {approach_angle}
# ESTIMATED IMPACT: {estimated_value}

# KEY INSIGHTS:
# {insights}

# Create a personalized, compelling email that will get a response.""")
#             ])
            
#             chain = prompt | self.llm
            
#             response = chain.invoke({
#                 "format_instructions": self.parser.get_format_instructions(),
#                 "name": client['name'],
#                 "company": client.get('company', 'Unknown'),
#                 "industry": client.get('industry', 'Unknown'),
#                 "opportunity_type": opportunity.opportunity_type,
#                 "timing_reason": opportunity.timing_reason,
#                 "approach_angle": opportunity.approach_angle,
#                 "estimated_value": opportunity.estimated_value,
#                 #"insights": '\n'.join(['- ' + i for i in opportunity.key_insights[:3]])
#             })
            
#             # Parse response
#             email_text = response.content
            
#             # Extract JSON from response
#             if "```json" in email_text:
#                 email_text = email_text.split("```json")[1].split("```")[0].strip()
#             elif "```" in email_text:
#                 email_text = email_text.split("```")[1].split("```")[0].strip()
            
#             email_dict = json.loads(email_text)
#             state["email_content"] = EmailContent(**email_dict)
#             print(f"✓ Email Writer Agent: Created email for {client['name']}")
            
#         except Exception as e:
#             state["errors"].append(f"Email Writer Agent error: {str(e)}")
#             # Fallback email
#             state["email_content"] = EmailContent(
#                 subject=f"Quick check-in - {opportunity.opportunity_type}",
#                 body=f"Hi {client['name']},\n\nI wanted to reach out regarding {opportunity.opportunity_type}. {opportunity.approach_angle}\n\nWould you have time for a brief call this week?\n\nBest regards,\nYour Financial Advisor",
#                 tone="professional",
#                 personalization_elements=["client name", "opportunity type"]
#             )
        
#         return state


# # ============================================================================
# # MULTI-AGENT WORKFLOW
# # ============================================================================

# class JarvisAgentSystem:
#     """Multi-agent system orchestrating the analysis workflow."""
    
#     def __init__(self):
#         """Initialize the agent system."""
#         self.llm = ChatGoogleGenerativeAI(
#             model="gemini-pro",
#             google_api_key=os.getenv("GOOGLE_API_KEY"),
#             temperature=0.7
#         )
#         self.rag = RAGSystem()
        
#         # Initialize agents
#         self.research_agent = ResearchAgent(self.rag)
#         self.analysis_agent = AnalysisAgent(self.llm)
#         self.email_writer_agent = EmailWriterAgent(self.llm)
        
#         # Build workflow graph
#         self.workflow = self._build_workflow()
        
#         self.data_dir = Path(__file__).parent.parent / "data"
    
#     def _build_workflow(self) -> StateGraph:
#         """Build the LangGraph workflow."""
#         workflow = StateGraph(AgentState)
        
#         # Add nodes (agents)
#         workflow.add_node("research", self.research_agent.execute)
#         workflow.add_node("analysis", self.analysis_agent.execute)
#         workflow.add_node("email_writer", self.email_writer_agent.execute)
        
#         # Define edges (workflow)
#         workflow.set_entry_point("research")
#         workflow.add_edge("research", "analysis")
#         workflow.add_edge("analysis", "email_writer")
#         workflow.add_edge("email_writer", END)
        
#         return workflow.compile()
    
#     def process_client(self, client: Dict[str, Any]) -> Dict[str, Any]:
#         """Process a single client through the agent workflow."""
#         print(f"\n🤖 Processing {client['name']}...")
        
#         # Initialize state
#         initial_state: AgentState = {
#             "client": client,
#             "rag_context": "",
#             "opportunity_analysis": None,
#             "email_content": None,
#             "errors": []
#         }
        
#         # Run workflow
#         final_state = self.workflow.invoke(initial_state)
        
#         # Extract results
#         opportunity = final_state["opportunity_analysis"]
#         email = final_state["email_content"]
        
#         if not opportunity or not email:
#             print(f"❌ Failed to process {client['name']}")
#             return None
        
#         # Create email record
#         email_id = f"email_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{client['client_id']}"
        
#         return {
#             "id": email_id,
#             "client_id": client['client_id'],
#             "client_name": client['name'],
#             "client_email": client['email'],
#             "subject": email.subject,
#             "body": email.body,
#             "preview": email.body[:150] + "...",
#             "full_content": email.body,
#             "sent_date": datetime.now().isoformat(),
#             "status": "sent",
#             "opportunity_type": opportunity.opportunity_type,
#             "priority_score": opportunity.priority_score,
#             "tone": email.tone,
#             "personalization_elements": email.personalization_elements,
#             "agent_workflow": "research → analysis → email_writer"
#         }
    
#     def overnight_analysis_run(self, top_n: int = 8) -> Dict[str, Any]:
#         """Run the overnight analysis using multi-agent workflow."""
#         print("\n" + "="*70)
#         print("🌙 JARVIS MULTI-AGENT SYSTEM - Overnight Analysis")
#         print("="*70)
        
#         # Load clients
#         client_file = self.data_dir / "client_context.json"
#         with open(client_file, 'r') as f:
#             clients = json.load(f)
        
#         print(f"\n📊 Analyzing {len(clients)} clients using agentic workflow...")
#         print("   Agents: Research → Analysis → Email Writer")
        
#         # Process each client through agent workflow
#         all_results = []
#         for i, client in enumerate(clients, 1):
#             print(f"\n[{i}/{len(clients)}] Client: {client['name']}")
#             result = self.process_client(client)
#             if result:
#                 all_results.append(result)
        
#         # Sort by priority score
#         all_results.sort(key=lambda x: x['priority_score'], reverse=True)
        
#         # Take top N
#         top_results = all_results[:top_n]
        
#         print(f"\n" + "="*70)
#         print(f"🎯 Top {top_n} Opportunities Selected")
#         print("="*70)
        
#         for i, result in enumerate(top_results, 1):
#             print(f"\n[{i}] {result['client_name']}")
#             print(f"    Opportunity: {result['opportunity_type']}")
#             print(f"    Priority: {result['priority_score']}/10")
#             print(f"    Subject: {result['subject']}")
        
#         # Save results
#         emails_file = self.data_dir / "emails_sent.json"
#         with open(emails_file, 'w') as f:
#             json.dump(top_results, f, indent=2)
        
#         print(f"\n" + "="*70)
#         print("✅ Multi-Agent Analysis Complete!")
#         print(f"   📧 {len(top_results)} emails generated")
#         print(f"   💾 Saved to {emails_file}")
#         print(f"   🤖 Powered by LangGraph agentic framework")
#         print("="*70 + "\n")
        
#         return {
#             "total_clients_analyzed": len(clients),
#             "emails_generated": len(top_results),
#             "agent_framework": "LangGraph",
#             "agents_used": ["ResearchAgent", "AnalysisAgent", "EmailWriterAgent"],
#             "workflow": "research → analysis → email_writer",
#             "top_opportunities": [
#                 {
#                     "client": r['client_name'],
#                     "opportunity": r['opportunity_type'],
#                     "priority": r['priority_score']
#                 }
#                 for r in top_results
#             ]
#         }


# def run_overnight_analysis():
#     """Standalone function to run the overnight analysis."""
#     system = JarvisAgentSystem()
#     return system.overnight_analysis_run(top_n=8)


# if __name__ == "__main__":
#     # Run the multi-agent analysis
#     results = run_overnight_analysis()
    
#     print("\n📊 SUMMARY")
#     print("="*70)
#     print(f"Framework: {results['agent_framework']}")
#     print(f"Agents: {', '.join(results['agents_used'])}")
#     print(f"Workflow: {results['workflow']}")
#     print(f"Clients Analyzed: {results['total_clients_analyzed']}")
#     print(f"Emails Generated: {results['emails_generated']}")
#     print("\nTop Opportunities:")
#     for opp in results['top_opportunities']:
#         print(f"  • {opp['client']}: {opp['opportunity']} (Priority: {opp['priority']}/10)")

"""
Agentic AI System using LangGraph
Multi-agent workflow for autonomous client analysis and outreach
"""
import os
import json
import re
from pathlib import Path
from typing import List, Dict, Any, TypedDict, Annotated
from datetime import datetime
import operator

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END
from rag_system import RAGSystem

# Load environment variables
load_dotenv()


# ============================================================================
# PYDANTIC MODELS FOR STRUCTURED OUTPUT
# ============================================================================

class OpportunityAnalysis(BaseModel):
    """Structured output for opportunity analysis."""
    client_id: str = Field(description="Client identifier")
    client_name: str = Field(description="Client name")
    opportunity_type: str = Field(description="Type of opportunity (e.g., 'Tax Planning', 'R&D Credits')")
    priority_score: int = Field(description="Priority score from 1-10", ge=1, le=10)
    timing_reason: str = Field(description="Why reach out now")
    approach_angle: str = Field(description="The hook/value proposition")
    estimated_value: str = Field(description="Potential $ impact or benefit")
    key_insights: List[str] = Field(description="Key insights about the client")


class EmailContent(BaseModel):
    """Structured output for email generation."""
    subject: str = Field(description="Email subject line")
    body: str = Field(description="Full email body")
    tone: str = Field(description="Tone of the email (professional/friendly/consultative)")
    personalization_elements: List[str] = Field(description="Specific personalization elements used")


# ============================================================================
# AGENT STATE
# ============================================================================

class AgentState(TypedDict):
    """State passed between agents in the workflow."""
    client: Dict[str, Any]
    rag_context: str
    opportunity_analysis: OpportunityAnalysis | None
    email_content: EmailContent | None
    errors: Annotated[List[str], operator.add]


# ============================================================================
# INDIVIDUAL AGENTS
# ============================================================================

class ResearchAgent:
    """Agent responsible for gathering context from RAG system."""
    
    def __init__(self, rag_system: RAGSystem):
        self.rag = rag_system
    
    def execute(self, state: AgentState) -> AgentState:
        """Research client using RAG system."""
        client = state["client"]
        
        try:
            # Build search query
            search_query = f"{client['name']} {client['company']} {' '.join(client.get('pain_points', []))}"
            
            # Search RAG
            rag_results = self.rag.search(search_query, n_results=5)
            
            # Combine context
            context = "\n\n".join([
                f"Document: {r['metadata'].get('source', 'Unknown')}\n{r['content']}"
                for r in rag_results
            ]) if rag_results else "No additional context available."
            
            state["rag_context"] = context[:2000]  # Limit context size
            print(f"✓ Research Agent: Gathered context for {client['name']}")
            
        except Exception as e:
            state["errors"].append(f"Research Agent error: {str(e)}")
            state["rag_context"] = "No context available."
        
        return state

class AnalysisAgent:
    """Agent responsible for analyzing opportunities."""
    
    def __init__(self, llm: ChatGoogleGenerativeAI):
        self.llm = llm
        self.parser = PydanticOutputParser(pydantic_object=OpportunityAnalysis)
    
    def execute(self, state: AgentState) -> AgentState:
        """Analyze client for opportunities."""
        client = state["client"]
        rag_context = state["rag_context"]
        
        try:
            prompt = ChatPromptTemplate.from_messages([
                ("system", """You are an expert financial advisor AI analyzing clients for proactive outreach opportunities.
                
Your task is to identify the MOST COMPELLING opportunity for this client based on:
1. Their current situation and recent activities
2. Pain points and challenges
3. Industry trends and timing
4. Potential financial impact

{format_instructions}"""),
                ("user", """Analyze this client:

CLIENT PROFILE:
Name: {name}
Company: {company}
Industry: {industry}
Revenue: {revenue}
Company Size: {size}

KEY INSIGHTS:
{insights}

PAIN POINTS:
{pain_points}

ADDITIONAL CONTEXT FROM DOCUMENTS:
{rag_context}

Identify the top opportunity and provide a structured analysis.""")
            ])
            
            chain = prompt | self.llm
            
            response = chain.invoke({
                "format_instructions": self.parser.get_format_instructions(),
                "name": client['name'],
                "company": client.get('company', 'Unknown'),
                "industry": client.get('industry', 'Unknown'),
                "revenue": client.get('revenue_range', 'Unknown'),
                "size": client.get('company_size', 'Unknown'),
                "insights": '\n'.join(['- ' + i for i in client.get('key_insights', [])]),
                "pain_points": '\n'.join(['- ' + p for p in client.get('pain_points', [])]),
                "rag_context": rag_context
            })
            
            # Parse response
            analysis_text = response.content
            
            # Extract JSON from response
            if "```json" in analysis_text:
                analysis_text = analysis_text.split("```json")[1].split("```")[0].strip()
            elif "```" in analysis_text:
                analysis_text = analysis_text.split("```")[1].split("```")[0].strip()
            
            analysis_dict = json.loads(analysis_text)
            analysis_dict['client_id'] = client['client_id']
            analysis_dict['client_name'] = client['name']
            
            state["opportunity_analysis"] = OpportunityAnalysis(**analysis_dict)
            print(f"✓ Analysis Agent: Identified {state['opportunity_analysis'].opportunity_type} for {client['name']}")
            
        except Exception as e:
            state["errors"].append(f"Analysis Agent error: {str(e)}")
            # Fallback analysis
            state["opportunity_analysis"] = OpportunityAnalysis(
                client_id=client['client_id'],
                client_name=client['name'],
                opportunity_type=client.get('pain_points', ['General Advisory'])[0] if client.get('pain_points') else 'General Advisory',
                priority_score=client.get('engagement_score', 50) // 10,
                timing_reason="Regular check-in based on client profile",
                approach_angle="Proactive advisory support",
                estimated_value="Ongoing relationship value",
                key_insights=client.get('key_insights', [])[:3]
            )
        
        return state


class EmailWriterAgent:
    """Agent responsible for writing personalized emails."""
    
    def __init__(self, llm: ChatGoogleGenerativeAI):
        self.llm = llm
        self.parser = PydanticOutputParser(pydantic_object=EmailContent)
    
    def _extract_json_from_response(self, text: str) -> Dict[str, Any]:
        """Extract JSON from LLM response with multiple fallback strategies."""
        
        # Strategy 1: Look for JSON code block
        if "```json" in text:
            json_text = text.split("```json")[1].split("```")[0].strip()
            try:
                return json.loads(json_text)
            except json.JSONDecodeError:
                pass
        
        # Strategy 2: Look for any code block
        if "```" in text:
            json_text = text.split("```")[1].split("```")[0].strip()
            # Remove language identifier if present
            lines = json_text.split('\n')
            if lines[0].strip() in ['json', 'JSON']:
                json_text = '\n'.join(lines[1:])
            try:
                return json.loads(json_text)
            except json.JSONDecodeError:
                pass
        
        # Strategy 3: Look for JSON object in text using regex
        json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
        matches = re.findall(json_pattern, text, re.DOTALL)
        for match in matches:
            try:
                return json.loads(match)
            except json.JSONDecodeError:
                continue
        
        # Strategy 4: Try parsing the entire text
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        
        raise ValueError("Could not extract valid JSON from response")
    
    def _parse_email_from_text(self, text: str, opportunity: OpportunityAnalysis, client: Dict[str, Any]) -> EmailContent:
        """Parse email content from unstructured text response."""
        
        # Try to extract subject line
        subject = ""
        subject_patterns = [
            r'subject[:\s]+([^\n]+)',
            r'Subject[:\s]+([^\n]+)',
            r'SUBJECT[:\s]+([^\n]+)',
            r'"subject"[:\s]+"([^"]+)"',
        ]
        
        for pattern in subject_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                subject = match.group(1).strip()
                break
        
        if not subject:
            subject = f"Quick check-in - {opportunity.opportunity_type}"
        
        # Try to extract body
        body = ""
        
        # Remove subject line from text
        text_without_subject = re.sub(r'subject[:\s]+[^\n]+', '', text, flags=re.IGNORECASE)
        
        # Look for body markers
        body_patterns = [
            r'body[:\s]+(.+)',
            r'Body[:\s]+(.+)',
            r'BODY[:\s]+(.+)',
            r'"body"[:\s]+"(.+?)"',
        ]
        
        for pattern in body_patterns:
            match = re.search(pattern, text_without_subject, re.IGNORECASE | re.DOTALL)
            if match:
                body = match.group(1).strip()
                # Clean up JSON artifacts
                body = body.replace('\\"', '"').replace('\\n', '\n')
                break
        
        # If no body found, use the text after cleaning
        if not body:
            # Remove JSON markers and clean up
            body = text_without_subject
            body = re.sub(r'```[a-z]*\n?', '', body)
            body = re.sub(r'\{[^}]*\}', '', body)
            body = body.strip()
        
        # If still no good body, create one
        if len(body) < 50:
            body = f"""Hi {client['name']},

I wanted to reach out regarding {opportunity.opportunity_type}. {opportunity.approach_angle}

{opportunity.timing_reason}

Would you have time for a brief call this week to discuss how we can help?

Best regards,
Your Financial Advisor"""
        
        # Determine tone
        tone = "professional"
        if any(word in body.lower() for word in ['hi', 'hey', 'hope you', 'looking forward']):
            tone = "friendly"
        if any(word in body.lower() for word in ['strategic', 'analysis', 'recommend']):
            tone = "consultative"
        
        # Identify personalization elements
        personalization = []
        if client['name'] in body:
            personalization.append("client name")
        if client.get('company', '') in body:
            personalization.append("company name")
        if opportunity.opportunity_type.lower() in body.lower():
            personalization.append("opportunity type")
        if any(insight[:20].lower() in body.lower() for insight in opportunity.key_insights):
            personalization.append("specific insights")
        
        return EmailContent(
            subject=subject,
            body=body,
            tone=tone,
            personalization_elements=personalization if personalization else ["basic personalization"]
        )
    
    def execute(self, state: AgentState) -> AgentState:
        """Generate personalized email."""
        client = state["client"]
        opportunity = state["opportunity_analysis"]
        
        if not opportunity:
            state["errors"].append("No opportunity analysis available")
            return state
        
        try:
            # Use a more directive prompt that's less likely to need JSON parsing
            prompt = ChatPromptTemplate.from_messages([
                ("system", """You are an expert email writer for financial advisors. Write warm, personalized outreach emails.

CRITICAL: You MUST respond with ONLY a valid JSON object. No other text before or after.

The JSON must have this exact structure:
{{
  "subject": "compelling subject line here",
  "body": "full email body here with proper greeting, context, value prop, and call to action",
  "tone": "professional or friendly or consultative",
  "personalization_elements": ["element1", "element2"]
}}

GUIDELINES FOR THE EMAIL:
- Warm and personal (not salesy)
- Show you've done research (reference specific insights)
- Clear value proposition
- Soft call-to-action (suggest a brief call)
- Professional but friendly tone
- Concise (150-200 words)
- Compelling subject line

Return ONLY the JSON object, nothing else."""),
                ("user", """Write an email for this client:

CLIENT: {name}
COMPANY: {company}
INDUSTRY: {industry}

OPPORTUNITY: {opportunity_type}
WHY NOW: {timing_reason}
VALUE PROPOSITION: {approach_angle}
ESTIMATED IMPACT: {estimated_value}

KEY INSIGHTS:
{insights}

Return ONLY valid JSON with subject, body, tone, and personalization_elements fields.""")
            ])
            
            chain = prompt | self.llm
            
            response = chain.invoke({
                "name": client['name'],
                "company": client.get('company', 'Unknown'),
                "industry": client.get('industry', 'Unknown'),
                "opportunity_type": opportunity.opportunity_type,
                "timing_reason": opportunity.timing_reason,
                "approach_angle": opportunity.approach_angle,
                "estimated_value": opportunity.estimated_value,
                "insights": '\n'.join(['- ' + i for i in opportunity.key_insights[:3]])
            })
            
            email_text = response.content
            
            # Try to extract and parse JSON
            try:
                email_dict = self._extract_json_from_response(email_text)
                state["email_content"] = EmailContent(**email_dict)
                print(f"✓ Email Writer Agent: Created email for {client['name']} (JSON parsed)")
                
            except (ValueError, json.JSONDecodeError) as parse_error:
                # Fallback: Parse from unstructured text
                print(f"  ⚠ JSON parsing failed, using text extraction for {client['name']}")
                state["email_content"] = self._parse_email_from_text(email_text, opportunity, client)
                print(f"✓ Email Writer Agent: Created email for {client['name']} (text extraction)")
            
        except Exception as e:
            error_msg = f"Email Writer Agent error: {str(e)}"
            print(f"  ❌ {error_msg}")
            state["errors"].append(error_msg)
            
            # Ultimate fallback email
            state["email_content"] = EmailContent(
                subject=f"Quick check-in - {opportunity.opportunity_type}",
                body=f"""Hi {client['name']},

I wanted to reach out regarding {opportunity.opportunity_type}. {opportunity.approach_angle}

{opportunity.timing_reason}

Would you have time for a brief call this week to discuss how we can help?

Best regards,
Your Financial Advisor""",
                tone="professional",
                personalization_elements=["client name", "opportunity type"]
            )
            print(f"✓ Email Writer Agent: Created fallback email for {client['name']}")
        
        return state


# ============================================================================
# MULTI-AGENT WORKFLOW
# ============================================================================

class JarvisAgentSystem:
    """Multi-agent system orchestrating the analysis workflow."""
    
    def __init__(self):
        """Initialize the agent system."""
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.7
        )
        self.rag = RAGSystem()
        
        # Initialize agents
        self.research_agent = ResearchAgent(self.rag)
        self.analysis_agent = AnalysisAgent(self.llm)
        self.email_writer_agent = EmailWriterAgent(self.llm)
        
        # Build workflow graph
        self.workflow = self._build_workflow()
        
        self.data_dir = Path(__file__).parent.parent / "data"
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow."""
        workflow = StateGraph(AgentState)
        
        # Add nodes (agents)
        workflow.add_node("research", self.research_agent.execute)
        workflow.add_node("analysis", self.analysis_agent.execute)
        workflow.add_node("email_writer", self.email_writer_agent.execute)
        
        # Define edges (workflow)
        workflow.set_entry_point("research")
        workflow.add_edge("research", "analysis")
        workflow.add_edge("analysis", "email_writer")
        workflow.add_edge("email_writer", END)
        
        return workflow.compile()
    
    def process_client(self, client: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single client through the agent workflow."""
        print(f"\n🤖 Processing {client['name']}...")
        
        # Initialize state
        initial_state: AgentState = {
            "client": client,
            "rag_context": "",
            "opportunity_analysis": None,
            "email_content": None,
            "errors": []
        }
        
        # Run workflow
        final_state = self.workflow.invoke(initial_state)
        
        # Extract results
        opportunity = final_state["opportunity_analysis"]
        email = final_state["email_content"]
        
        if not opportunity or not email:
            print(f"❌ Failed to process {client['name']}")
            return None
        
        # Create email record
        email_id = f"email_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{client['client_id']}"
        
        return {
            "id": email_id,
            "client_id": client['client_id'],
            "client_name": client['name'],
            "client_email": client['email'],
            "subject": email.subject,
            "body": email.body,
            "preview": email.body[:150] + "...",
            "full_content": email.body,
            "sent_date": datetime.now().isoformat(),
            "status": "sent",
            "opportunity_type": opportunity.opportunity_type,
            "priority_score": opportunity.priority_score,
            "tone": email.tone,
            "personalization_elements": email.personalization_elements,
            "agent_workflow": "research → analysis → email_writer"
        }
    
    def overnight_analysis_run(self, top_n: int = 8) -> Dict[str, Any]:
        """Run the overnight analysis using multi-agent workflow."""
        print("\n" + "="*70)
        print("🌙 JARVIS MULTI-AGENT SYSTEM - Overnight Analysis")
        print("="*70)
        
        # Load clients
        client_file = self.data_dir / "client_context.json"
        with open(client_file, 'r') as f:
            clients = json.load(f)
        
        print(f"\n📊 Analyzing {len(clients)} clients using agentic workflow...")
        print("   Agents: Research → Analysis → Email Writer")
        
        # Process each client through agent workflow
        all_results = []
        for i, client in enumerate(clients, 1):
            print(f"\n[{i}/{len(clients)}] Client: {client['name']}")
            result = self.process_client(client)
            if result:
                all_results.append(result)
        
        # Sort by priority score
        all_results.sort(key=lambda x: x['priority_score'], reverse=True)
        
        # Take top N
        top_results = all_results[:top_n]
        
        print(f"\n" + "="*70)
        print(f"🎯 Top {top_n} Opportunities Selected")
        print("="*70)
        
        for i, result in enumerate(top_results, 1):
            print(f"\n[{i}] {result['client_name']}")
            print(f"    Opportunity: {result['opportunity_type']}")
            print(f"    Priority: {result['priority_score']}/10")
            print(f"    Subject: {result['subject']}")
        
        # Save results
        emails_file = self.data_dir / "emails_sent.json"
        with open(emails_file, 'w') as f:
            json.dump(top_results, f, indent=2)
        
        print(f"\n" + "="*70)
        print("✅ Multi-Agent Analysis Complete!")
        print(f"   📧 {len(top_results)} emails generated")
        print(f"   💾 Saved to {emails_file}")
        print(f"   🤖 Powered by LangGraph agentic framework")
        print("="*70 + "\n")
        
        return {
            "total_clients_analyzed": len(clients),
            "emails_generated": len(top_results),
            "agent_framework": "LangGraph",
            "agents_used": ["ResearchAgent", "AnalysisAgent", "EmailWriterAgent"],
            "workflow": "research → analysis → email_writer",
            "top_opportunities": [
                {
                    "client": r['client_name'],
                    "opportunity": r['opportunity_type'],
                    "priority": r['priority_score']
                }
                for r in top_results
            ]
        }


def run_overnight_analysis():
    """Standalone function to run the overnight analysis."""
    system = JarvisAgentSystem()
    return system.overnight_analysis_run(top_n=8)


if __name__ == "__main__":
    # Run the multi-agent analysis
    results = run_overnight_analysis()
    
    print("\n📊 SUMMARY")
    print("="*70)
    print(f"Framework: {results['agent_framework']}")
    print(f"Agents: {', '.join(results['agents_used'])}")
    print(f"Workflow: {results['workflow']}")
    print(f"Clients Analyzed: {results['total_clients_analyzed']}")
    print(f"Emails Generated: {results['emails_generated']}")
    print("\nTop Opportunities:")
    for opp in results['top_opportunities']:
        print(f"  • {opp['client']}: {opp['opportunity']} (Priority: {opp['priority']}/10)")