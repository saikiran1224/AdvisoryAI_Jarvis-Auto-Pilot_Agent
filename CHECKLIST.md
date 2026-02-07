# ✅ Pre-Demo Checklist

## 🔧 Setup (Do This First!)

- [ ] **Install Dependencies**
  ```bash
  ./setup.sh
  ```

- [ ] **Add Gemini API Key**
  - Edit `backend/.env`
  - Add: `GOOGLE_API_KEY=your_key_here`

- [ ] **Add Client Documents**
  - Place DOCX files in `data/client_documents/`
  - Or use the sample documents provided

- [ ] **Run AI Analysis**
  ```bash
  ./run_analysis.sh
  ```
  - This takes 5-10 minutes
  - Generates emails and warm leads

---

## 🧪 Testing (Before Demo!)

- [ ] **Start the Application**
  ```bash
  ./run.sh
  ```

- [ ] **Test Backend**
  - Open: http://localhost:8000
  - Should see API info
  - Check: http://localhost:8000/docs

- [ ] **Test Frontend**
  - Open: http://localhost:5173
  - Should see dashboard
  - Check all metrics load

- [ ] **Test Features**
  - [ ] Metrics display correctly
  - [ ] Warm leads show up
  - [ ] Can click on a lead
  - [ ] Modal opens with details
  - [ ] Activity feed works
  - [ ] Refresh button works

- [ ] **Test on Mobile**
  - [ ] Open on phone/tablet
  - [ ] Check responsive layout
  - [ ] Test interactions

---

## 📊 Data Verification

- [ ] **Check Generated Emails**
  ```bash
  cat data/emails_sent.json | jq
  ```
  - Should have 8 emails
  - Each with subject and body

- [ ] **Check Responses**
  ```bash
  cat data/responses.json | jq
  ```
  - Should have 3 responses
  - Each with sentiment and priority

- [ ] **Check Client Context**
  ```bash
  cat data/client_context.json | jq
  ```
  - Should have 5 clients
  - Each with full profile

---

## 🎬 Demo Preparation

- [ ] **Practice Demo Flow**
  1. Show dashboard metrics
  2. Click on warm lead
  3. Show email Jarvis sent
  4. Show client response
  5. Show context for call
  6. Explain the value

- [ ] **Prepare Talking Points**
  - [ ] "AI that ACTS, not just advises"
  - [ ] "Autonomous overnight analysis"
  - [ ] "Warm leads ready by morning"
  - [ ] "Advisor didn't do ANY of this"

- [ ] **Time Your Demo**
  - [ ] Full demo: 3 minutes
  - [ ] Quick version: 90 seconds
  - [ ] Extended: 5 minutes

- [ ] **Prepare for Questions**
  - How does RAG work?
  - What AI model do you use?
  - How do you ensure email quality?
  - What about compliance?
  - Can it integrate with CRM?

---

## 🚀 Deployment (Optional)

- [ ] **Deploy Backend to Railway**
  - Create Railway project
  - Connect GitHub repo
  - Add `GOOGLE_API_KEY` env var
  - Deploy

- [ ] **Deploy Frontend to Vercel**
  - Create Vercel project
  - Connect GitHub repo
  - Add `VITE_API_URL` env var
  - Deploy

- [ ] **Test Production**
  - [ ] Backend API works
  - [ ] Frontend loads
  - [ ] Data displays correctly

---

## 📱 Presentation Setup

- [ ] **Computer Setup**
  - [ ] Charge laptop fully
  - [ ] Test projector connection
  - [ ] Increase screen brightness
  - [ ] Close unnecessary apps

- [ ] **Browser Setup**
  - [ ] Clear browser cache
  - [ ] Zoom to 125% for visibility
  - [ ] Bookmark dashboard URL
  - [ ] Test all interactions

- [ ] **Backup Plan**
  - [ ] Screenshot key screens
  - [ ] Record demo video
  - [ ] Have localhost running
  - [ ] Bring USB with code

---

## 🎯 Day-Of Checklist

### 2 Hours Before
- [ ] Start application (`./run.sh`)
- [ ] Verify all features work
- [ ] Practice demo one more time

### 1 Hour Before
- [ ] Check internet connection
- [ ] Test on presentation computer
- [ ] Have backup ready

### 30 Minutes Before
- [ ] Refresh dashboard
- [ ] Clear browser console
- [ ] Take deep breath 😊

### 5 Minutes Before
- [ ] Open dashboard in browser
- [ ] Have API docs ready (backup)
- [ ] Smile and be confident!

---

## 🎤 Demo Script Reminder

**Opening (30 sec):**
> "Advisors know they should be proactive. They never get around to it. We built an AI that IS proactive FOR them."

**Demo (2 min):**
1. Show metrics: "8 emails sent autonomously"
2. Click warm lead: "Sarah Chen responded"
3. Show context: "Full background for the call"
4. The kicker: "Advisor didn't do ANY of this"

**Closing (30 sec):**
> "While the advisor sleeps, Jarvis creates warm conversations. By morning, they have 5 calls ready to make. That's not advice. That's action."

---

## ✅ Final Checks

- [ ] Application running smoothly
- [ ] All features tested
- [ ] Demo practiced
- [ ] Talking points memorized
- [ ] Questions prepared
- [ ] Backup ready
- [ ] Confident and excited!

---

## 🆘 Emergency Contacts

**If something breaks:**
1. Check logs: `tail -f backend/logs.txt`
2. Restart: `./run.sh`
3. Use backup: Screenshots/video
4. Stay calm and explain the concept

---

## 🎉 You Got This!

Remember:
- **You built something amazing** in 2 hours
- **The idea is strong** - autonomous AI agent
- **The execution is solid** - working prototype
- **The presentation matters** - tell the story

**Good luck! 🚀**

---

## 📞 Quick Commands

```bash
# Start everything
./run.sh

# Run analysis
./run_analysis.sh

# Check backend
curl http://localhost:8000/api/stats

# Check frontend
open http://localhost:5173

# View logs
tail -f backend/logs.txt

# Restart
pkill -f "python app.py"
pkill -f "vite"
./run.sh
```

---

**Last updated:** Right before your demo!
**Status:** READY TO WIN! 🏆
