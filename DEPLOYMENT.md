# 🚀 Deployment Guide

## Quick Deploy Checklist

### Prerequisites
- [ ] Google Gemini API Key
- [ ] GitHub account
- [ ] Railway account (for backend)
- [ ] Vercel account (for frontend)

---

## 🔧 Backend Deployment (Railway)

### Step 1: Prepare Repository
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### Step 2: Deploy to Railway

1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Select the `backend` folder as root
6. Add environment variable:
   - Key: `GOOGLE_API_KEY`
   - Value: Your Gemini API key

7. Railway will auto-deploy!

### Step 3: Get Your Backend URL

After deployment, Railway will give you a URL like:
```
https://your-app.railway.app
```

Copy this URL - you'll need it for the frontend!

---

## 🎨 Frontend Deployment (Vercel)

### Step 1: Update Environment Variable

Edit `frontend/.env.production`:
```
VITE_API_URL=https://your-app.railway.app
```

Replace with your actual Railway backend URL.

### Step 2: Deploy to Vercel

#### Option A: Vercel CLI
```bash
cd frontend
npm install -g vercel
vercel --prod
```

#### Option B: Vercel Dashboard
1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import your GitHub repository
4. Set root directory to `frontend`
5. Add environment variable:
   - Key: `VITE_API_URL`
   - Value: Your Railway backend URL
6. Click "Deploy"

### Step 3: Access Your App

Vercel will give you a URL like:
```
https://your-app.vercel.app
```

🎉 Your app is live!

---

## 🧪 Testing Deployment

### Test Backend
```bash
curl https://your-app.railway.app/api/stats
```

Should return JSON with statistics.

### Test Frontend
Open your Vercel URL in a browser. You should see the dashboard!

---

## 🔐 Environment Variables Summary

### Backend (Railway)
```
GOOGLE_API_KEY=your_gemini_api_key_here
```

### Frontend (Vercel)
```
VITE_API_URL=https://your-backend.railway.app
```

---

## 📊 Post-Deployment Setup

### 1. Add Client Documents

You'll need to upload your client DOCX files. Options:

**Option A: Include in Git** (if files are not sensitive)
```bash
# Add files to data/client_documents/
git add data/client_documents/*.docx
git commit -m "Add client documents"
git push
```

**Option B: Upload via API** (recommended for production)
Create an upload endpoint or use Railway's file storage.

### 2. Run Initial Analysis

SSH into Railway or use the API:
```bash
curl -X POST https://your-app.railway.app/api/ingest-documents
curl -X POST https://your-app.railway.app/api/run-analysis
```

---

## 🐛 Troubleshooting

### Backend Issues

**Problem:** 500 errors
- Check Railway logs
- Verify `GOOGLE_API_KEY` is set
- Check if dependencies installed correctly

**Problem:** CORS errors
- Verify frontend URL is allowed in CORS settings
- Check `app.py` CORS configuration

### Frontend Issues

**Problem:** Can't connect to backend
- Verify `VITE_API_URL` is correct
- Check if backend is running
- Test backend URL directly

**Problem:** Build fails
- Check Node.js version (need 18+)
- Clear node_modules and reinstall
- Check for syntax errors

---

## 🔄 Updating Your App

### Update Backend
```bash
git add backend/
git commit -m "Update backend"
git push
```
Railway auto-deploys on push!

### Update Frontend
```bash
git add frontend/
git commit -m "Update frontend"
git push
```
Vercel auto-deploys on push!

---

## 💰 Cost Estimate

### Free Tier
- **Railway**: $5 free credit/month (enough for demo)
- **Vercel**: Unlimited for personal projects
- **Gemini API**: Free tier available

### Paid (if needed)
- **Railway**: ~$10-20/month for production
- **Vercel**: Free for most use cases
- **Gemini API**: Pay per use

---

## 🎯 Demo Day Tips

### Before Your Presentation

1. **Pre-load data**: Run analysis beforehand
2. **Test everything**: Click through all features
3. **Have backup**: Keep localhost running too
4. **Check mobile**: Test on phone/tablet

### During Presentation

1. **Start with metrics**: Show the dashboard first
2. **Click a warm lead**: Demonstrate the full flow
3. **Show the email**: Let them see Jarvis's work
4. **Explain the value**: "Advisor didn't do ANY of this"

### Backup Plan

If deployment fails:
```bash
# Run locally
./run.sh
```

Use ngrok to share:
```bash
ngrok http 5173
```

---

## 📞 Support

- Railway Docs: https://docs.railway.app
- Vercel Docs: https://vercel.com/docs
- Gemini API: https://ai.google.dev/docs

---

**Good luck with your hackathon! 🚀**
