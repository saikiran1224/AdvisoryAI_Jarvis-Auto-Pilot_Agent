# ⚡ Quick Start Guide - 2 Hour Hackathon Build

## 🎯 Goal
Get Jarvis Auto-Pilot running with your client documents in under 10 minutes!

---

## 📋 Prerequisites (5 minutes)

### 1. Get Google Gemini API Key
1. Go to https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key

### 2. Add Your API Key
```bash
# Edit backend/.env
nano backend/.env

# Add this line (replace with your actual key):
GOOGLE_API_KEY=your_actual_gemini_api_key_here

# Save and exit (Ctrl+X, then Y, then Enter)
```

---

## 🚀 Installation (3 minutes)

```bash
# Run the setup script
./setup.sh
```

This installs all dependencies for both backend and frontend.

---

## 📚 Add Your Client Documents (2 minutes)

```bash
# Copy your DOCX files to the client_documents folder
cp /path/to/your/documents/*.docx data/client_documents/

# Or create the folder and add files manually
open data/client_documents/
```

**Note:** The system works best with documents that contain:
- Client profiles
- Financial information
- Recent activities
- Pain points or opportunities

---

## 🤖 Run the Agents (5-10 minutes)

```bash
# This will:
# 1. Ingest your documents into RAG
# 2. Run LangGraph Multi-Agent System
# 3. Research → Analysis → Email Writer
./run_analysis.sh
```

**What happens (Multi-Agent Workflow):**
- 🕵️ **Research Agent**: Scans documents for relevant context
- 🧠 **Analysis Agent**: Identifies top opportunities based on insights
- ✍️ **Writer Agent**: Crafts personalized emails for each client
- ✅ Results saved to `data/emails_sent.json`

---

## 🎨 Launch the Dashboard (1 minute)

```bash
# Start both backend and frontend
./run.sh
```

Then open your browser to:
- **Dashboard:** http://localhost:5173
- **API Docs:** http://localhost:8000/docs

---

## 🎯 Demo Flow (For Your Presentation)

### 1. Show the Dashboard
- **Metrics:** "Jarvis sent 8 emails autonomously"
- **Warm Leads:** "3 clients already responded"
- **Activity Feed:** "See the timeline of actions"

### 2. Click on a Warm Lead
- **Show what Jarvis did:** The email it sent
- **Show client response:** Their interested reply
- **Show the context:** Full background for the call
- **The kicker:** "The advisor didn't do ANY of this"

### 3. Explain the Value
> "Traditional tools tell advisors to be proactive. Jarvis IS proactive FOR them. While they sleep, Jarvis analyzes 200 clients, identifies opportunities, and creates warm conversations. By morning, the advisor has 5 calls ready to make."

---

## 🔧 Troubleshooting

### "Module not found" errors
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### "API key not found"
```bash
# Make sure backend/.env exists and has your key
cat backend/.env
```

### "No documents found"
```bash
# Check if DOCX files are in the right place
ls data/client_documents/
```

### Frontend won't start
```bash
cd frontend
rm -rf node_modules
npm install
npm run dev
```

---

## 📊 What You'll See

### Metrics Dashboard
- 📧 **Emails Sent:** 8 (autonomous outreach)
- 💬 **Responses:** 3 (60% response rate!)
- 🎯 **Warm Leads:** 3 (ready to call)
- 👥 **Clients Analyzed:** 5

### Warm Lead Card Example
```
🎯 Sarah Chen - TechStartup.io
Priority: HIGH | Sentiment: POSITIVE

Timeline:
✓ 8:00 AM - Jarvis sent email about tax planning
✓ 2:14 PM - Sarah responded (interested!)

Response: "Thanks for reaching out! This is exactly 
what we need right now. Can we schedule a call?"

Next Action: [Schedule Call]
Engagement Score: 85/100
```

---

## 🎬 Presentation Script

**Opening (30 seconds):**
> "Advisors know they should be proactive. They just never get around to it. We built an AI that IS proactive FOR them."

**Demo (2 minutes):**
1. Show dashboard metrics
2. Click on warm lead
3. Show full context
4. Explain the autonomous flow

**Closing (30 seconds):**
> "While the advisor sleeps, Jarvis analyzes 200 clients, identifies opportunities, and autonomously sends personalized outreach. By morning, the advisor has 5 warm conversations ready to happen. That's not helping advisors be proactive—that's BEING proactive on their behalf."

---

## 🚀 Advanced: Customize the Data

### Edit Client Profiles
```bash
nano data/client_context.json
```

### Edit Mock Responses
```bash
nano data/responses.json
```

### Re-run Analysis
```bash
./run_analysis.sh
```

---

## 📱 Mobile Testing

The dashboard is fully responsive! Test on:
- iPhone/iPad
- Android devices
- Different screen sizes

---

## ⏱️ Timeline Recap

- **0-5 min:** Get API key, add to .env
- **5-8 min:** Run setup script
- **8-10 min:** Add documents
- **10-20 min:** Run AI analysis
- **20-22 min:** Launch dashboard
- **22-30 min:** Test and prepare demo

**Total: 30 minutes to fully working demo!**

---

## 🎯 Success Checklist

- [ ] API key added to backend/.env
- [ ] Setup script completed successfully
- [ ] Client documents added to data/client_documents/
- [ ] AI analysis ran without errors
- [ ] Dashboard loads at localhost:5173
- [ ] Can see metrics and warm leads
- [ ] Can click on leads and see details
- [ ] Prepared 3-minute demo script

---

## 🆘 Need Help?

### Check Logs
```bash
# Backend logs
tail -f backend/logs.txt

# Frontend console
# Open browser DevTools (F12)
```

### Test API Directly
```bash
# Check if backend is running
curl http://localhost:8000/

# Get dashboard data
curl http://localhost:8000/api/dashboard

# Get stats
curl http://localhost:8000/api/stats
```

---

## 🎉 You're Ready!

Your Jarvis Auto-Pilot Agent is now running and ready to demo!

**Pro Tips:**
- Practice your demo 2-3 times
- Have backup data ready
- Test on the presentation computer
- Bring a video recording as backup

**Good luck! 🚀**
