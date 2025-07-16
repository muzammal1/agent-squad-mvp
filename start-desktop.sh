#!/bin/bash
echo "🖥️ Starting Agent Squad MVP Desktop Interface..."
echo "Access the app at: http://localhost:8501"
echo "Press Ctrl+C to stop"
source venv/bin/activate
streamlit run main-app.py
