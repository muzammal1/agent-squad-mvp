#!/bin/bash

# Setup Script for Agent Squad MVP
# This script sets up the complete environment for development

echo "🤖 Agent Squad MVP Setup"
echo "======================="
echo ""

# Check Python version
echo "🐍 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.8 or higher and run this script again."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing requirements..."
pip install -r requirements.txt

# Copy environment file
echo "⚙️ Setting up environment configuration..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✅ Created .env file from template"
    echo "🔑 Please edit .env file with your API keys before running the application"
else
    echo "ℹ️ .env file already exists"
fi

# Create necessary directories
echo "📁 Creating directory structure..."
mkdir -p logs
mkdir -p data
mkdir -p mobile/public
mkdir -p mobile/.chainlit

# Set up pre-commit hooks (optional)
echo "🔧 Setting up development tools..."
pip install pre-commit black flake8
cat > .pre-commit-config.yaml << EOF
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=88, --extend-ignore=E203,W503]
EOF

# Install pre-commit hooks
pre-commit install

# Test installation
echo "🧪 Testing installation..."
python -c "import streamlit; import agent_squad; print('✅ Core dependencies installed successfully')"

# Create quick start scripts
echo "🚀 Creating quick start scripts..."

# Desktop app launcher
cat > start-desktop.sh << 'EOF'
#!/bin/bash
echo "🖥️ Starting Agent Squad MVP Desktop Interface..."
echo "Access the app at: http://localhost:8501"
echo "Press Ctrl+C to stop"
source venv/bin/activate
streamlit run main-app.py
EOF

# Make scripts executable
chmod +x start-desktop.sh
chmod +x deploy-mobile.sh

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next Steps:"
echo "1. Edit .env file with your API keys:"
echo "   - ANTHROPIC_API_KEY (required for Claude models)"
echo "   - NEONPANEL_API_KEY (for NeonPanel integration)"
echo "   - AWS credentials (optional, for Bedrock models)"
echo ""
echo "2. Start the application:"
echo "   Desktop: ./start-desktop.sh"
echo "   Mobile:  ./deploy-mobile.sh"
echo ""
echo "3. Access the applications:"
echo "   Desktop: http://localhost:8501"
echo "   Mobile:  http://localhost:8000"
echo ""
echo "📖 Documentation:"
echo "   - README.md for project overview"
echo "   - Check individual agent demos in subdirectories"
echo "   - MCP integration docs in mcp/ directory"
echo ""
echo "🆘 Need help?"
echo "   - Check logs/ directory for error logs"
echo "   - Ensure all API keys are correctly configured"
echo "   - Verify internet connectivity for external APIs"
