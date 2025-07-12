# Netlify + Backend Split Deployment Guide

## 🎯 Strategy: Best of Both Worlds

### Frontend (Netlify) + Backend (Railway/Render)
- **Frontend**: React app on Netlify (FREE, permanent link)
- **Backend**: FastAPI on Railway/Render ($0-5/month)
- **Result**: Professional setup with CDN performance

## 🚀 Deployment Steps

### Step 1: Deploy Backend First

#### Option A: Railway (Recommended)
1. Go to [railway.app](https://railway.app)
2. Connect your GitHub repo
3. Deploy the full project (ignores frontend folder)
4. Get backend URL: `https://your-app.railway.app`

#### Option B: Render
1. Go to [render.com](https://render.com)
2. Create Web Service from GitHub
3. Use root directory, Docker environment
4. Get backend URL: `https://your-app.onrender.com`

### Step 2: Update Frontend API URL

Update `frontend/src/ResumeAnalyzerForm.js` and `frontend/src/CandidateRanking.js`:

```javascript
// Change this line:
const API_BASE_URL = 'http://localhost:8001';

// To your deployed backend:
const API_BASE_URL = 'https://your-app.railway.app';
// or
const API_BASE_URL = 'https://your-app.onrender.com';
```

### Step 3: Deploy Frontend to Netlify

1. **Go to [netlify.com](https://netlify.com)**
2. **Sign up with GitHub**
3. **"Add new site" → "Import from Git"**
4. **Select your repository**
5. **Configure build settings:**
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `frontend/build`
6. **Deploy!**

### Step 4: Get Your Links

- **Frontend**: `https://your-app.netlify.app` (FREE forever)
- **Backend**: `https://your-app.railway.app` (FREE trial, then $5/month)
- **API Docs**: `https://your-app.railway.app/docs`

## 💰 Cost Breakdown

### Free Option:
- **Netlify Frontend**: FREE forever
- **Render Backend**: FREE (sleeps after 15min)
- **Total**: $0/month

### Production Option:
- **Netlify Frontend**: FREE forever  
- **Railway Backend**: $5/month (always active + database)
- **Total**: $5/month

## 🌟 Benefits of This Setup

### Performance
- **CDN**: Netlify serves frontend from global CDN
- **Speed**: Frontend loads instantly worldwide
- **SEO**: Better search engine optimization

### Reliability
- **99.9% Uptime**: Both platforms are enterprise-grade
- **Auto-scaling**: Handles traffic spikes automatically
- **SSL**: Free HTTPS on both platforms

### Professional URLs
- **Frontend**: `https://resume-analyzer.netlify.app`
- **Backend**: `https://resume-analyzer-api.railway.app`
- **Custom domains**: Available on both platforms

## 🔧 Advanced Configuration

### Environment Variables on Netlify
```bash
# In Netlify dashboard → Site settings → Environment variables
REACT_APP_API_URL=https://your-backend.railway.app
REACT_APP_VERSION=1.0.0
```

### Custom Domains
```bash
# Frontend: yoursite.com
# Backend: api.yoursite.com
```

## 🎯 Why This Is Better Than Single Platform

1. **Cost**: Frontend hosting is FREE forever
2. **Performance**: CDN makes frontend super fast
3. **Scalability**: Each part scales independently
4. **Reliability**: If one service has issues, the other works
5. **Professional**: Industry-standard architecture

## 🚀 Quick Start Commands

```bash
# 1. Deploy backend to Railway/Render (use existing setup)

# 2. Update frontend API URL
cd frontend/src
# Edit API_BASE_URL in ResumeAnalyzerForm.js and CandidateRanking.js

# 3. Commit changes
git add .
git commit -m "Update API URL for production"
git push

# 4. Deploy frontend to Netlify (via web interface)
```

This gives you a professional, scalable setup that's either FREE or very low cost!
