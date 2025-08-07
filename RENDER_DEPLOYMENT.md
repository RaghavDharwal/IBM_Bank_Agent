# Render Deployment Guide for IBM Bank Agent

This guide will help you deploy the AI-Powered Banking Portal to Render.

## Prerequisites

1. **GitHub Repository**: Your code must be pushed to GitHub
2. **Render Account**: Sign up at [render.com](https://render.com)
3. **Email Configuration**: SMTP settings for email notifications

## Deployment Steps

### 1. Prepare Your Repository

Ensure these files are in your repository root:
- `requirements.txt` ✅ (Created)
- `render.yaml` ✅ (Created) 
- `Procfile` ✅ (Created)
- `.gitignore` ✅ (Updated)

### 2. Environment Variables Setup

You'll need to configure these environment variables in Render:

#### Required Variables:
```
PORT=10000
SECRET_KEY=your-secret-key-here
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
BANK_EMAIL=your-bank-email@gmail.com
BANK_NAME=AI Banking Portal
```

#### Optional Variables:
```
API_KEY=your-ibm-watson-api-key
AGENT_ENDPOINT=your-watson-agent-url
```

### 3. Deploy to Render

#### Option A: Using render.yaml (Recommended)
1. Push your code to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Click "New" → "Blueprint"
4. Connect your GitHub repository
5. Render will automatically detect `render.yaml`
6. Review the configuration and click "Apply"

#### Option B: Manual Setup
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `cd backend && python agent.py`
   - **Environment**: `Python 3`

### 4. Configure Environment Variables

In your Render service dashboard:
1. Go to "Environment" tab
2. Add all the required environment variables listed above
3. For `SECRET_KEY`, you can generate a secure key or let Render generate one

### 5. Email Setup (Gmail Example)

For Gmail SMTP:
1. Enable 2-Factor Authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a new app password for "Mail"
3. Use this app password (not your regular password) for `SMTP_PASSWORD`

### 6. Deploy and Test

1. Click "Create Web Service"
2. Render will build and deploy your application
3. Once deployed, you'll get a public URL like: `https://your-app-name.onrender.com`
4. Test all features:
   - LoanBot chatbot
   - User registration/login
   - Loan application
   - Admin dashboard
   - Email notifications

## Post-Deployment Configuration

### Database Migration (Optional)
For production, consider migrating from CSV files to a proper database:
- PostgreSQL (Render provides free PostgreSQL)
- SQLite for simple setups

### File Storage
- For production file uploads, consider using cloud storage (AWS S3, Cloudinary)
- Current setup stores files locally (will be lost on restart)

### Security Enhancements
1. Use strong `SECRET_KEY`
2. Enable HTTPS (automatic on Render)
3. Configure proper CORS origins
4. Use environment-specific configurations

## Troubleshooting

### Common Issues:

1. **Build Failure**:
   - Check `requirements.txt` for correct package versions
   - Ensure Python version compatibility

2. **App Won't Start**:
   - Verify `PORT` environment variable is set
   - Check start command in render.yaml or manual config

3. **Email Not Working**:
   - Verify SMTP credentials
   - Check if 2FA and app passwords are set up correctly
   - Test SMTP settings locally first

4. **Static Files Not Loading**:
   - Ensure frontend files are in the repository
   - Check static file routes in agent.py

### Logs and Debugging:
- View logs in Render dashboard under "Logs" tab
- Enable debug mode temporarily for detailed error messages
- Check email logs for SMTP issues

## Cost Considerations

- **Free Tier**: 750 hours/month (enough for demo/development)
- **Production**: Consider paid plans for better performance
- **Database**: Free PostgreSQL with 1GB storage

## Support

For deployment issues:
1. Check Render documentation: [render.com/docs](https://render.com/docs)
2. Review application logs in Render dashboard
3. Test locally first to isolate deployment vs. application issues

## Success Checklist

After deployment, verify:
- [ ] Application loads at Render URL
- [ ] All three pages work (index.html, apply.html, staff.html)
- [ ] User registration/login works
- [ ] Admin login works
- [ ] Email notifications are sent
- [ ] File uploads work (for basic testing)
- [ ] Database operations (CSV read/write) work
- [ ] All environment variables are set correctly

Your AI-Powered Banking Portal should now be live and accessible worldwide! 🚀
