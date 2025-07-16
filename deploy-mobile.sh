#!/bin/bash

# Mobile Deployment Script for Agent Squad MVP
# This script prepares and deploys the mobile-ready chat interface

echo "🚀 Agent Squad MVP - Mobile Deployment"
echo "======================================"

# Check if we're in the right directory
if [ ! -f "main-app.py" ]; then
    echo "❌ Error: Please run this script from the agent-squad-mvp directory"
    exit 1
fi

# Create mobile directory if it doesn't exist
mkdir -p mobile

# Copy and prepare mobile files
echo "📱 Preparing mobile interface..."
cp -r chat-ui/* mobile/
cd mobile

# Install mobile-specific dependencies
echo "📦 Installing dependencies..."
pip install chainlit streamlit-chat streamlit-elements

# Create mobile-optimized chainlit config
cat > .chainlit/config.toml << EOF
[project]
enable_telemetry = false

[UI]
name = "Agent Squad MVP"
default_expand_messages = true
default_collapse_content = false
hide_cot = false
wide_mode = false

[meta]
generated_by = "1.0.0"

[features]
multi_modal = true
speech_to_text = 
  enabled = false
  language = "en"
EOF

# Create mobile-specific startup script
cat > start-mobile.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting Agent Squad MVP Mobile Interface..."
echo "Access the app at: http://localhost:8000"
echo "Press Ctrl+C to stop"
chainlit run app.py --host 0.0.0.0 --port 8000
EOF

chmod +x start-mobile.sh

# Create PWA manifest for mobile app
cat > public/manifest.json << EOF
{
  "name": "Agent Squad MVP",
  "short_name": "AgentSquad",
  "description": "Multi-Agent Chat System",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#4CAF50",
  "icons": [
    {
      "src": "/logo.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any maskable"
    }
  ]
}
EOF

# Create mobile-optimized CSS
cat > public/style.css << EOF
/* Mobile-optimized styles for Agent Squad MVP */
:root {
  --primary-color: #4CAF50;
  --secondary-color: #2196F3;
  --background-color: #f5f5f5;
  --text-color: #333;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
  .main-container {
    padding: 8px;
    margin: 0;
  }
  
  .chat-message {
    font-size: 14px;
    padding: 8px 12px;
    margin-bottom: 8px;
    border-radius: 12px;
    max-width: 85%;
  }
  
  .user-message {
    background-color: var(--primary-color);
    color: white;
    margin-left: auto;
    margin-right: 8px;
  }
  
  .assistant-message {
    background-color: white;
    color: var(--text-color);
    margin-right: auto;
    margin-left: 8px;
    border: 1px solid #e0e0e0;
  }
  
  .input-container {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: white;
    padding: 12px;
    border-top: 1px solid #e0e0e0;
  }
  
  .agent-indicator {
    font-size: 12px;
    color: var(--secondary-color);
    font-weight: bold;
    margin-bottom: 4px;
  }
}

/* Touch-friendly buttons */
.action-button {
  min-height: 44px;
  min-width: 44px;
  border-radius: 8px;
  border: none;
  background-color: var(--primary-color);
  color: white;
  font-size: 16px;
  cursor: pointer;
  touch-action: manipulation;
}

.action-button:hover {
  background-color: #45a049;
}

/* Loading indicator */
.loading {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
EOF

echo "✅ Mobile interface prepared successfully!"
echo ""
echo "📱 To start the mobile interface:"
echo "   cd mobile && ./start-mobile.sh"
echo ""
echo "🌐 To start the desktop interface:"
echo "   streamlit run main-app.py"
echo ""
echo "🔧 Don't forget to:"
echo "   1. Copy .env.example to .env and configure your API keys"
echo "   2. Install dependencies: pip install -r requirements.txt"
echo "   3. Test the NeonPanel MCP connection"
