"""
Client Sync Script (Mock CRM Integration)
-----------------------------------------
Automatically updates client_context.json based on the documents found in data/client_documents.
This simulates a real-world CRM syncing with your document management system.

Usage: python sync_clients.py
"""
import os
import json
import random
from pathlib import Path
from datetime import datetime

# Configuration
DATA_DIR = Path("data")
DOCS_DIR = DATA_DIR / "client_documents"
CONTEXT_FILE = DATA_DIR / "client_context.json"

def clean_name(filename):
    """Extract a clean client name from a filename."""
    # Remove extension
    stem = Path(filename).stem
    
    # Replace underscores and dashes with spaces
    name = stem.replace("_", " ").replace("-", " ")
    
    # Remove common suffixes to isolate the name
    suffixes = ["profile", "planning", "opportunity", "agreement", "report", "tax", "advisory", "rd", "exit"]
    parts = name.split()
    
    clean_parts = []
    for part in parts:
        if part.lower() not in suffixes:
            clean_parts.append(part)
            
    # Rejoin and title case (e.g., "david park" -> "David Park")
    return " ".join(clean_parts).title()

def generate_mock_profile(name):
    """Generate a realistic mock profile for a new client."""
    first_name = name.split()[0] if name else "Client"
    last_name = name.split()[-1] if len(name.split()) > 1 else ""
    
    industries = ["Technology", "Healthcare", "Manufacturing", "Real Estate", "Professional Services"]
    
    return {
        "client_id": f"client_{random.randint(1000, 9999)}",
        "name": name,
        "email": f"{first_name.lower()}.{last_name.lower()}@example.com",
        "company": f"{last_name} Enterprises" if last_name else f"{first_name} Co",
        "industry": random.choice(industries),
        "revenue_range": "$1M - $10M",
        "company_size": "10-50 employees",
        "key_insights": ["New client detected from document upload"],
        "pain_points": ["Needs comprehensive tax review"],
        "engagement_score": 50,  # Neutral starting score
        "last_interaction": datetime.now().strftime("%Y-%m-%d")
    }

def sync_clients():
    print("🔄 Syncing Client List from Documents...")
    
    # 1. Load existing clients to preserve data
    existing_clients = []
    if CONTEXT_FILE.exists():
        try:
            with open(CONTEXT_FILE, 'r') as f:
                existing_clients = json.load(f)
        except json.JSONDecodeError:
            print("⚠️  Warning: Existing client_context.json was invalid. Starting fresh.")
    
    # Create a map of normalized names to existing records for easy lookup
    existing_map = {c["name"].lower(): c for c in existing_clients}
    
    # 2. Scan documents
    if not DOCS_DIR.exists():
        print(f"❌ Document directory not found: {DOCS_DIR}")
        return

    doc_files = list(DOCS_DIR.glob("*.docx"))
    if not doc_files:
        print("⚠️  No documents found to sync.")
        return
        
    print(f"📂 Found {len(doc_files)} documents.")
    
    new_count = 0
    
    for doc in doc_files:
        # Extract name from filename
        client_name = clean_name(doc.name)
        
        # Check if client already exists
        if client_name.lower() in existing_map:
            # Client exists, maybe update last interaction?
            # For now, we skip to preserve manual CRM data
            continue
            
        # Create new client record
        print(f"➕ Detected new client: {client_name}")
        new_profile = generate_mock_profile(client_name)
        existing_clients.append(new_profile)
        existing_map[client_name.lower()] = new_profile # Update map to prevent duplicates if multiple files exist
        new_count += 1
        
    # 3. Save updated list
    if new_count > 0:
        with open(CONTEXT_FILE, 'w') as f:
            json.dump(existing_clients, f, indent=2)
        print(f"✅ added {new_count} new clients to CRM (client_context.json).")
    else:
        print("✅ Client list is up to date.")

if __name__ == "__main__":
    sync_clients()
