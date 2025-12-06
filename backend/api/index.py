"""
Vercel serverless function entry point.
This file allows the FastAPI app to run on Vercel's serverless platform.
"""

from app.main import app

# Vercel expects the app to be available as 'app' or 'handler'
handler = app
