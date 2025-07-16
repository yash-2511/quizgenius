# Deployment Checklist for AI Quiz Generator

Use this checklist to ensure successful deployment to Render.

## Pre-Deployment Checklist

### ✅ Code Preparation
- [ ] All code is committed to Git
- [ ] Repository is pushed to GitHub
- [ ] No sensitive data (API keys) in code
- [ ] All dependencies listed in `render_requirements.txt`

### ✅ Configuration Files
- [ ] `render_requirements.txt` - Production dependencies
- [ ] `Procfile` - Gunicorn startup command
- [ ] `runtime.txt` - Python 3.11.0
- [ ] `render.yaml` - Render configuration (optional)
- [ ] `main.py` - Proper entry point

### ✅ Environment Variables Required
- [ ] `GEMINI_API_KEY` - Your Google Gemini API key
- [ ] `FLASK_ENV` - Set to "production"
- [ ] `FLASK_DEBUG` - Set to "false"
- [ ] `SESSION_SECRET` - Secure random string

### ✅ Application Health
- [ ] Health endpoint `/health` responds
- [ ] Main page loads without errors
- [ ] File upload validation works
- [ ] Quiz generation works locally

## Deployment Process

### Step 1: Render Setup
- [ ] Render account created
- [ ] GitHub connected to Render
- [ ] Repository selected for deployment

### Step 2: Service Configuration
- [ ] Service name: `ai-quiz-generator` (or your choice)
- [ ] Environment: Python 3
- [ ] Build Command: `pip install -r render_requirements.txt`
- [ ] Start Command: `gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 0 main:app`

### Step 3: Environment Variables
- [ ] All required environment variables added
- [ ] API key is valid and working
- [ ] Session secret is secure (32+ characters)

### Step 4: Deploy
- [ ] Initial deployment started
- [ ] Build logs checked for errors
- [ ] Application starts successfully
- [ ] No startup errors in logs

## Post-Deployment Testing

### ✅ Basic Functionality
- [ ] App URL is accessible
- [ ] Health check: `https://your-app.onrender.com/health`
- [ ] Main page loads completely
- [ ] CSS and JavaScript files load

### ✅ File Upload Testing
- [ ] Upload form is visible
- [ ] File validation works (rejects .txt files)
- [ ] PDF upload works (if you have a test PDF)
- [ ] DOCX upload works (if you have a test DOCX)

### ✅ Quiz Generation
- [ ] Text extraction works
- [ ] Gemini API responds
- [ ] Quiz questions display
- [ ] Answer submission works
- [ ] Results show with explanations

### ✅ Quiz History
- [ ] Quiz history loads
- [ ] Previous quizzes are accessible
- [ ] No errors in quiz retrieval

## Production Monitoring

### ✅ Performance
- [ ] App responds within acceptable time
- [ ] No memory or timeout errors
- [ ] Cold start time acceptable (< 60 seconds)

### ✅ Error Handling
- [ ] Error pages display properly
- [ ] Invalid file uploads handled gracefully
- [ ] API failures show user-friendly messages
- [ ] Large file uploads rejected properly

### ✅ Security
- [ ] HTTPS is working (automatic on Render)
- [ ] No API keys exposed in logs
- [ ] File uploads are properly validated
- [ ] Session handling is secure

## Troubleshooting Common Issues

### Build Failures
- [ ] Check Python version compatibility
- [ ] Verify all dependencies in requirements file
- [ ] Review build logs for specific errors

### Runtime Errors
- [ ] Check application logs in Render dashboard
- [ ] Verify environment variables are set
- [ ] Test Gemini API key validity

### Performance Issues
- [ ] Monitor response times
- [ ] Check memory usage
- [ ] Review worker configuration

## Test Commands

Run these commands to verify deployment:

```bash
# Test health endpoint
curl https://your-app.onrender.com/health

# Test main page
curl -I https://your-app.onrender.com/

# Run full deployment test
python test_deployment.py https://your-app.onrender.com
```

## Success Criteria

Your deployment is successful when:
- [ ] All endpoints respond correctly
- [ ] File uploads work end-to-end
- [ ] Quiz generation completes successfully
- [ ] No critical errors in logs
- [ ] Application is publicly accessible

## Next Steps After Deployment

### ✅ Optional Enhancements
- [ ] Custom domain setup
- [ ] Database integration (PostgreSQL)
- [ ] Error monitoring (Sentry)
- [ ] Analytics integration
- [ ] Performance monitoring
- [ ] Backup strategy

### ✅ Maintenance
- [ ] Monitor application logs
- [ ] Set up alerts for downtime
- [ ] Plan for regular updates
- [ ] Monitor API usage limits

---

## Emergency Contacts

- **Render Support**: [community.render.com](https://community.render.com)
- **Google Gemini API**: [ai.google.dev](https://ai.google.dev)
- **Project Repository**: Your GitHub repository URL

---

**Note**: Keep this checklist updated as you make changes to the deployment process.