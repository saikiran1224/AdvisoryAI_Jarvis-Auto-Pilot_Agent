# Jarvis Auto-Pilot Agent 🚀

**AI that acts FOR you, not just advises**

## 🎯 The Concept

Jarvis autonomously reaches out to clients on your behalf, then brings you back high-quality, warm conversations ready to close.

### How It Works:

**9:00 AM - Jarvis Analyzes**
- Scans all client documents using RAG
- Identifies high-value opportunities
- Prioritizes based on urgency and impact

**9:15 AM - Jarvis ACTS (Autonomously)**
- Drafts personalized emails using AI
- SENDS them (in demo mode, simulated)
- Logs all actions for compliance

**2:30 PM - Client Responds**
- "Thanks! Yes, I'd love to discuss. When are you free?"

**2:31 PM - Jarvis Notifies You**
- 🎯 WARM LEAD READY
- Full context provided
- Suggested next actions
- One-click to schedule

## 🏗️ Architecture

```
├── backend/                 # FastAPI Server
│   ├── app.py              # Main API endpoints
│   ├── agentic_system.py   # LangGraph Multi-Agent System
│   ├── rag_system.py         # Document ingestion & search
│   └── requirements.txt
│
├── frontend/               # React + Vite
│   ├── src/
│   │   ├── App.jsx        # Main dashboard
│   │   ├── App.css        # Component styles
│   │   └── index.css      # Design system
│   └── package.json
│
└── data/
    ├── client_documents/   # DOCX files (your documents)
    ├── client_context.json # Client profiles
    ├── emails_sent.json    # Generated emails
    └── responses.json      # Mock responses
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- Google Gemini API Key

### Backend Setup

```bash
# Install Python dependencies
cd backend
pip install -r requirements.txt

# Set up environment variables
cp ../.env.example .env
# Edit .env and add your GOOGLE_API_KEY

# Run the server
python app.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

```bash
# Install dependencies
cd frontend
npm install

# Run development server
npm run dev
```

The dashboard will be available at `http://localhost:5173`

## 📚 Adding Your Client Documents

1. Place your DOCX files in `data/client_documents/`
2. Run the ingestion:
   ```bash
   cd backend
   python -c "from rag_system import ingest_documents; ingest_documents()"
   ```

## 🤖 Running the AI Agent

### Overnight Analysis (Demo)

```bash
cd backend
python ai_agent.py
```

This will:
1. Analyze all clients using RAG + Gemini
2. Identify top 8 opportunities
3. Generate personalized emails
4. Save to `data/emails_sent.json`

### Via API

```bash
curl -X POST http://localhost:8000/api/run-analysis
```

## 📊 API Endpoints

- `GET /api/dashboard` - Complete dashboard data
- `GET /api/warm-leads` - All warm leads with context
- `GET /api/emails` - All sent emails
- `GET /api/responses` - All client responses
- `GET /api/clients` - All client profiles
- `GET /api/stats` - Dashboard statistics
- `GET /api/activity` - Recent activity timeline
- `POST /api/run-analysis` - Trigger AI analysis
- `POST /api/ingest-documents` - Ingest DOCX files
- `GET /api/rag-stats` - RAG system statistics

## 🌐 Deployment

### Frontend (Vercel)

```bash
cd frontend
npm run build

# Deploy to Vercel
vercel --prod
```

Update `.env.production` with your backend URL.

### Backend (Railway)

1. Create a new project on Railway
2. Connect your GitHub repo
3. Set environment variables:
   - `GOOGLE_API_KEY=your_key_here`
4. Railway will auto-deploy

## 🎨 Features

✅ **RAG-Powered Analysis** - Ingests client documents for context  
✅ **AI Email Generation** - Gemini creates personalized outreach  
✅ **Warm Lead Detection** - Identifies interested clients  
✅ **Beautiful Dashboard** - Modern, professional UI  
✅ **Real-time Updates** - Live activity feed  
✅ **Context for Calls** - Full client background  
✅ **Priority Scoring** - Focus on high-value opportunities  
✅ **Sentiment Analysis** - Understand client responses  

## 🎯 Demo Flow

1. **Add Documents**: Place client DOCX files in `data/client_documents/`
2. **Ingest**: Run RAG ingestion
3. **Analyze**: Run overnight analysis
4. **View Dashboard**: See warm leads and metrics
5. **Take Action**: Click on leads to see full context

## 📝 Environment Variables

### Backend (.env)
```
GOOGLE_API_KEY=your_gemini_api_key_here
```

### Frontend (.env.production)
```
VITE_API_URL=https://your-backend-url.railway.app
```

## 🔧 Tech Stack

**Backend:**
- FastAPI - Modern Python web framework
- Google Gemini - AI model for analysis & generation
- ChromaDB - Vector database for RAG
- python-docx - Document parsing

**Frontend:**
- React 18 - UI library
- Vite - Build tool
- Lucide React - Icon library
- Axios - HTTP client

## 📄 License

MIT License - feel free to use for your hackathon!

## 🙋‍♂️ Support

For issues or questions, check the API docs at `http://localhost:8000/docs`

---

