#!/bin/bash

echo "🚀 Agent Squad MVP - One-Click Demo Deployment"
echo "=============================================="

echo "Which deployment option would you like?"
echo "1) Streamlit Cloud (FREE, 2 min)"
echo "2) Railway ($5/mo, 5 min)" 
echo "3) Docker Local (FREE, 1 min)"
echo "4) View all options"

read -p "Choose option (1-4): " choice

case $choice in
  1)
    echo "📝 Streamlit Cloud deployment:"
    echo "1. Push this code to GitHub"
    echo "2. Go to https://share.streamlit.io/"
    echo "3. Create new app with main file: main-app.py"
    echo "4. Your demo will be live at: https://your-app.streamlit.app"
    ;;
  2)
    echo "🚀 Railway deployment..."
    if ! command -v railway &> /dev/null; then
        echo "Installing Railway CLI..."
        npm install -g @railway/cli
    fi
    railway login
    railway init
    railway up
    ;;
  3)
    echo "🐳 Docker local deployment..."
    docker build -t agent-squad-mvp .
    echo "Starting container on port 8501..."
    docker run -p 8501:8501 agent-squad-mvp
    echo "Demo available at: http://localhost:8501"
    ;;
  4)
    echo "📖 Opening deployment guide..."
    open DEMO_DEPLOY.md
    ;;
  *)
    echo "Invalid option. Please choose 1-4."
    ;;
esac
