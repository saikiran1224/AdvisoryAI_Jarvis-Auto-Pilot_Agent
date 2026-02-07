import json
from pathlib import Path

DATA_DIR = Path("data")
EMAILS_FILE = DATA_DIR / "emails_sent.json"
RESPONSES_FILE = DATA_DIR / "responses.json"

def fix_leads():
    if not EMAILS_FILE.exists() or not RESPONSES_FILE.exists():
        print("Files not found.")
        return

    with open(EMAILS_FILE, 'r') as f:
        emails = json.load(f)
    
    with open(RESPONSES_FILE, 'r') as f:
        responses = json.load(f)

    print(f"Loaded {len(emails)} emails and {len(responses)} responses.")
    
    updated_count = 0
    
    for response in responses:
        client_email = response.get("client_email")
        if not client_email:
            continue
            
        # Find matching email
        matching_email = next((e for e in emails if e.get("client_email") == client_email), None)
        
        if matching_email:
            print(f"Linking response from {response['client_name']} to email {matching_email['id']}")
            response["email_id"] = matching_email["id"]
            updated_count += 1
        else:
            print(f"No matching email found for {response['client_name']}")

    if updated_count > 0:
        with open(RESPONSES_FILE, 'w') as f:
            json.dump(responses, f, indent=4)
        print(f"✅ Successfully linked {updated_count} warm leads.")
    else:
        print("No matches found to link.")

if __name__ == "__main__":
    fix_leads()
