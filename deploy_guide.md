# Render Deployment Guide for AI Quiz Generator

This guide will walk you through deploying your AI Quiz Generator to Render, a cloud platform that offers free hosting for web applications.

## Prerequisites

1. **GitHub Account** - Your code needs to be in a GitHub repository
2. **Render Account** - Sign up at [render.com](https://render.com)
3. **Gemini API Key** - From [Google AI Studio](https://makersuite.google.com/app/apikey)

## Step 1: Prepare Your Repository

1. **Create a GitHub repository** and push your code:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: AI Quiz Generator"
   git remote add origin https://github.com/yourusername/ai-quiz-generator.git
   git push -u origin main
   ```

2. **Verify deployment files** are in your repository:
   - `render_requirements.txt` - Python dependencies
   - `Procfile` - Render startup command
   - `render.yaml` - Render configuration (optional)
   - `runtime.txt` - Python version specification

## Step 2: Deploy to Render

### Method 1: Using Render Dashboard (Recommended)

1. **Go to [render.com](https://render.com)** and sign in

2. **Connect GitHub**: 
   - Click "New +" → "Web Service"
   - Connect your GitHub account
   - Select your AI Quiz Generator repository

3. **Configure the service**:
   ```
   Name: ai-quiz-generator (or your preferred name)
   Environment: Python 3
   Build Command: pip install -r render_requirements.txt
   Start Command: gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 0 main:app
   ```

4. **Set Environment Variables**:
   - Click "Advanced" → "Add Environment Variable"
   - Add these variables:
     ```
     GEMINI_API_KEY = your_actual_gemini_api_key_here
     FLASK_ENV = production
     FLASK_DEBUG = false
     SESSION_SECRET = your_secure_random_string_here
     ```

5. **Deploy**:
   - Click "Create Web Service"
   - Wait for the build to complete (5-10 minutes)
   - Your app will be available at: `https://your-app-name.onrender.com`

### Method 2: Using render.yaml (Infrastructure as Code)

1. **Push the `render.yaml` file** to your repository

2. **In Render Dashboard**:
   - Click "New +" → "Blueprint"
   - Connect your repository
   - Render will automatically detect the `render.yaml` file

3. **Add environment variables** as described above

## Step 3: Configure Environment Variables

In your Render service dashboard, add these environment variables:

| Variable | Value | Description |
|----------|-------|-------------|
| `GEMINI_API_KEY` | `AIza...` | Your Google Gemini API key |
| `FLASK_ENV` | `production` | Sets production mode |
| `FLASK_DEBUG` | `false` | Disables debug mode |
| `SESSION_SECRET` | `random_secure_string` | Flask session security |

### Generating a Session Secret

Use this command to generate a secure session secret:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## Step 4: Test Your Deployment

1. **Access your app** at the provided Render URL
2. **Test file upload** with a PDF or DOCX file
3. **Verify quiz generation** works properly
4. **Check logs** in Render dashboard if issues occur

## Step 5: Domain Setup (Optional)

1. **Custom Domain**:
   - In your service settings, go to "Custom Domains"
   - Add your domain (requires DNS configuration)

2. **HTTPS**: Render provides free SSL certificates automatically

## Troubleshooting

### Common Issues

1. **Build Failed**:
   - Check `render_requirements.txt` has correct package versions
   - Verify Python version in `runtime.txt` is supported
   - Check build logs for specific error messages

2. **App Won't Start**:
   - Verify the start command in Procfile
   - Check that `main:app` correctly references your Flask app
   - Review application logs

3. **Environment Variables**:
   - Ensure `GEMINI_API_KEY` is set correctly
   - Verify the API key is valid and active
   - Check all required environment variables are present

4. **File Upload Issues**:
   - Render has disk space limitations
   - The app cleans up uploaded files automatically
   - Check file size limits (16MB max)

### Checking Logs

1. Go to your service in Render dashboard
2. Click "Logs" tab
3. Monitor real-time logs for errors
4. Use logs to debug any issues

### Performance Optimization

1. **Free Tier Limitations**:
   - Apps sleep after 15 minutes of inactivity
   - Cold starts may take 30+ seconds
   - Limited to 512MB RAM

2. **Paid Tier Benefits**:
   - No sleeping
   - Faster startup times
   - More RAM and CPU

## Environment Differences

### Local vs Production

| Feature | Local | Production (Render) |
|---------|-------|---------------------|
| Debug Mode | Enabled | Disabled |
| Port | 5000 | Dynamic ($PORT) |
| Environment | development | production |
| SSL | No | Yes (automatic) |
| File Storage | Local disk | Ephemeral |

## Monitoring and Maintenance

1. **Health Checks**:
   - Render automatically monitors your app
   - App will restart if it becomes unresponsive

2. **Updates**:
   - Push to GitHub to trigger automatic redeploys
   - Monitor deployment status in dashboard

3. **Backups**:
   - Quiz data is stored in-memory (resets on restart)
   - Consider adding a database for persistence

## Security Considerations

1. **Environment Variables**:
   - Never commit API keys to Git
   - Use Render's environment variable system
   - Rotate keys periodically

2. **HTTPS**:
   - All traffic is encrypted automatically
   - No additional configuration needed

3. **File Upload Security**:
   - File type validation in place
   - Size limits enforced
   - Files automatically cleaned up

## Next Steps

1. **Database Integration**: Consider adding PostgreSQL for persistent storage
2. **Monitoring**: Set up error tracking (Sentry, etc.)
3. **Backup Strategy**: Implement data persistence
4. **Performance**: Monitor and optimize based on usage

## Support

- **Render Documentation**: [docs.render.com](https://docs.render.com)
- **Community**: [community.render.com](https://community.render.com)
- **Status Page**: [status.render.com](https://status.render.com)

---

Your AI Quiz Generator should now be successfully deployed and accessible worldwide through Render!