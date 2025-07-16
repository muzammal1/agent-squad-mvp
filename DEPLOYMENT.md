# Agent Squad MVP - Deployment Guide

## 🚀 **DEMO DEPLOYMENT OPTIONS** (Start Here!)

### ⭐ **Option 1: Streamlit Community Cloud (RECOMMENDED)**

**Best for**: Free demo deployment with easy sharing

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Agent Squad MVP Demo"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/agent-squad-mvp.git
   git push -u origin main
   ```

2. **Deploy in 2 minutes**:
   - Go to https://share.streamlit.io/
   - Click "New app" 
   - Connect GitHub repo
   - Main file: `main-app.py`
   - Click "Deploy!"

3. **Add Environment Variables** (Optional):
   ```
   ANTHROPIC_API_KEY=your_key_here
   AWS_ACCESS_KEY_ID=your_key_here
   AWS_SECRET_ACCESS_KEY=your_key_here
   ```

**Result**: `https://your-app.streamlit.app` (FREE!)

### 🔥 **Option 2: Railway (5 minutes, $5/month)**

1. **One-command deploy**:
   ```bash
   npm install -g @railway/cli
   railway login
   railway init
   railway up
   ```

**Result**: `https://your-app.railway.app`

### 🌐 **Option 3: Render (Free tier available)**

1. **Connect repo** at https://render.com
2. **Web Service** → GitHub repo
3. **Start Command**: `streamlit run main-app.py --server.port=$PORT --server.address=0.0.0.0`

**Result**: `https://your-app.onrender.com`

---

## 🎯 Deployment Options

This guide covers different deployment scenarios for your Agent Squad MVP.

### 1. Local Development

**Quick Start:**
```bash
cd agent-squad-mvp
./setup.sh
./start-desktop.sh
```

**Manual Setup:**
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run desktop app
streamlit run main-app.py

# Or run mobile app
cd chat-ui
chainlit run app.py
```

### 2. Mobile-Optimized Deployment

```bash
./deploy-mobile.sh
cd mobile
./start-mobile.sh
```

Access at: `http://localhost:8000`

### 3. Docker Deployment

**Create Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Expose ports
EXPOSE 8501 8000

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Default command (can be overridden)
CMD ["streamlit", "run", "main-app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**Build and run:**
```bash
# Build the image
docker build -t agent-squad-mvp .

# Run desktop version
docker run -p 8501:8501 agent-squad-mvp

# Run mobile version
docker run -p 8000:8000 agent-squad-mvp chainlit run chat-ui/app.py --host 0.0.0.0 --port 8000
```

### 4. AWS ECS Deployment

**Task Definition (task-definition.json):**
```json
{
  "family": "agent-squad-mvp",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::YOUR_ACCOUNT:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "agent-squad-app",
      "image": "YOUR_ACCOUNT.dkr.ecr.REGION.amazonaws.com/agent-squad-mvp:latest",
      "portMappings": [
        {
          "containerPort": 8501,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {"name": "ANTHROPIC_API_KEY", "value": "YOUR_KEY"},
        {"name": "NEONPANEL_API_KEY", "value": "YOUR_KEY"}
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/agent-squad-mvp",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

**Deploy to ECS:**
```bash
# Create ECR repository
aws ecr create-repository --repository-name agent-squad-mvp

# Build and push image
docker build -t agent-squad-mvp .
docker tag agent-squad-mvp:latest YOUR_ACCOUNT.dkr.ecr.REGION.amazonaws.com/agent-squad-mvp:latest
docker push YOUR_ACCOUNT.dkr.ecr.REGION.amazonaws.com/agent-squad-mvp:latest

# Create ECS service
aws ecs create-service \
  --cluster your-cluster \
  --service-name agent-squad-mvp \
  --task-definition agent-squad-mvp \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

### 5. Railway/Render/Heroku Deployment

**For Railway:**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

**For Render:**
1. Connect your GitHub repository
2. Set environment variables in Render dashboard
3. Use build command: `pip install -r requirements.txt`
4. Use start command: `streamlit run main-app.py --server.port $PORT --server.address 0.0.0.0`

### 6. Production Configuration

**Environment Variables:**
```bash
# Required
ANTHROPIC_API_KEY=your_anthropic_key
NEONPANEL_API_KEY=your_neonpanel_key
NEONPANEL_BASE_URL=https://api.neonpanel.com

# Optional
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
OPENAI_API_KEY=your_openai_key

# Production settings
DEBUG=false
APP_VERSION=1.0.0
```

**Security Considerations:**
- Use secrets management (AWS Secrets Manager, HashiCorp Vault)
- Enable HTTPS/TLS
- Set up proper authentication
- Configure CORS appropriately
- Use environment-specific configurations

### 7. Monitoring and Logging

**Add logging configuration:**
```python
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
```

**Health checks:**
```python
# Add to main-app.py
@st.cache_data
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": os.getenv("APP_VERSION", "1.0.0")
    }
```

### 8. Load Balancing and Scaling

**NGINX Configuration (nginx.conf):**
```nginx
upstream agent_squad {
    server app1:8501;
    server app2:8501;
}

server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://agent_squad;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Docker Compose for scaling:**
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - NEONPANEL_API_KEY=${NEONPANEL_API_KEY}
    deploy:
      replicas: 3
      restart_policy:
        condition: on-failure
```

## 🚀 Quick Deployment Commands

**Local Development:**
```bash
./setup.sh && ./start-desktop.sh
```

**Mobile Development:**
```bash
./deploy-mobile.sh
```

**Docker:**
```bash
docker build -t agent-squad-mvp . && docker run -p 8501:8501 agent-squad-mvp
```

**Production:**
```bash
# Set environment variables first
export ANTHROPIC_API_KEY="your_key"
export NEONPANEL_API_KEY="your_key"

# Deploy to your preferred platform
railway up  # or render deploy, or aws ecs update-service
```
