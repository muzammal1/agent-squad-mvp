#!/bin/bash

echo "🚀 Agent Squad MVP Launcher"
echo "=========================="

# Navigate to the correct directory
cd "$(dirname "$0")"

echo "📁 Current directory: $(pwd)"

# Check if required packages are installed
echo "🔍 Checking dependencies..."

python3 -c "import streamlit" 2>/dev/null || {
    echo "📦 Installing streamlit..."
    pip3 install streamlit
}

python3 -c "import agent_squad" 2>/dev/null || {
    echo "📦 Installing agent-squad..."
    pip3 install agent-squad
}

python3 -c "import dotenv" 2>/dev/null || {
    echo "📦 Installing python-dotenv..."
    pip3 install python-dotenv
}

echo "✅ All dependencies ready!"

# Copy environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your API keys"
fi

echo ""
echo "🌐 Starting Agent Squad MVP..."
echo "📱 Access the app at: http://localhost:8501"
echo "⏹️  Press Ctrl+C to stop"
echo ""

# Run the application
python3 -m streamlit run main-app.py --server.port 8501
