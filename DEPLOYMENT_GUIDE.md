# Railway Deployment Guide

## Quick Deployment Steps

### 1. Prepare Your Repository
```bash
# Make sure your code is committed
git add .
git commit -m "Ready for Railway deployment"
git push origin main
```

### 2. Deploy to Railway
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "Deploy from GitHub repo"
4. Select your AI-Powered-Resume-Analyzer repository
5. Railway will automatically detect your Dockerfile

### 3. Add Database (Optional)
1. In Railway dashboard, click "New" → "Database" → "PostgreSQL"
2. Railway will provide DATABASE_URL automatically
3. Update your database.py to use PostgreSQL instead of SQLite

### 4. Configure Environment Variables
In Railway dashboard, add these variables:
- `PORT`: 8001
- `LOG_LEVEL`: INFO
- `PYTHONPATH`: /app

### 5. Custom Domain (Optional)
1. In Railway dashboard, go to Settings
2. Add your custom domain
3. Railway handles SSL certificates automatically

## Alternative: Render Deployment

### 1. Create render.yaml
```yaml
services:
  - type: web
    name: resume-analyzer
    env: docker
    plan: free  # or starter for $7/month
    healthCheckPath: /health
    envVars:
      - key: PORT
        value: 8001
      - key: LOG_LEVEL  
        value: INFO

databases:
  - name: resume-analyzer-db
    plan: free  # 90 days free, then $7/month
```

### 2. Deploy Steps
1. Push code to GitHub
2. Go to [render.com](https://render.com)
3. Connect GitHub repository
4. Render auto-deploys from render.yaml

## Cost Comparison

### Railway
- **Free tier**: Limited hours
- **Hobby tier**: $5/month (recommended)
- **Pro tier**: $20/month (high traffic)

### Render  
- **Free tier**: Good for testing
- **Starter tier**: $7/month for web service
- **Database**: $7/month for PostgreSQL

### Total Monthly Cost
- **Railway**: ~$5-10/month (with database)
- **Render**: ~$14/month (web + database)
- **DigitalOcean**: ~$12/month (app + database)

## Recommendation
**Start with Railway** for simplicity and cost-effectiveness. You can always migrate later if needed.

## Production Checklist
- [ ] Environment variables configured
- [ ] Database connected (PostgreSQL recommended)
- [ ] Health check endpoint working (/health)
- [ ] SSL certificate active (automatic)
- [ ] Custom domain configured (optional)
- [ ] Monitoring setup (Railway provides basic metrics)
- [ ] Backup strategy for database
- [ ] Error tracking (consider Sentry integration)
