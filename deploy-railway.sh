#!/bin/bash

# Quick Deploy to Railway
echo "🚀 Deploying Agent Squad MVP to Railway..."

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "📦 Installing Railway CLI..."
    npm install -g @railway/cli
fi

# Login and deploy
echo "🔑 Please login to Railway..."
railway login

echo "🚀 Initializing and deploying..."
railway init
railway up

echo "✅ Deployment complete! Check your Railway dashboard for the URL."
echo "🌐 Your app will be available at: https://your-app.railway.app"
