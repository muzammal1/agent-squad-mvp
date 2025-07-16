# 🚀 DEMO DEPLOYMENT GUIDE

## **OPTION 1: Streamlit Community Cloud (RECOMMENDED)**

**⏱️ Time**: 2 minutes | **💰 Cost**: FREE | **🎯 Best for**: Quick demos

### Step-by-Step:

1. **Push to GitHub**:
   ```bash
   cd /Users/applepc/Documents/POc/agent-squad-mvp
   git init
   git add .
   git commit -m "Agent Squad MVP Demo"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/agent-squad-mvp.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**:
   - Go to https://share.streamlit.io/
   - Click "New app"
   - Choose "From existing repo"
   - Repository: `YOUR_USERNAME/agent-squad-mvp`
   - Branch: `main`
   - Main file path: `main-app.py`
   - Click "Deploy!"

3. **Your demo will be live at**: `https://agent-squad-mvp.streamlit.app`

---

## **OPTION 2: Railway (FASTEST FULL-STACK)**

**⏱️ Time**: 5 minutes | **💰 Cost**: $5/month | **🎯 Best for**: Production demos

### Step-by-Step:

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Deploy**:
   ```bash
   cd /Users/applepc/Documents/POc/agent-squad-mvp
   ./deploy-railway.sh
   ```

3. **Your demo will be live at**: `https://agent-squad-mvp.railway.app`

---

## **OPTION 3: Render (GOOD BALANCE)**

**⏱️ Time**: 3 minutes | **💰 Cost**: FREE (with sleep) | **🎯 Best for**: Portfolio demos

### Step-by-Step:

1. **Connect GitHub**: Go to https://render.com → New Web Service
2. **Settings**:
   - Repository: `YOUR_USERNAME/agent-squad-mvp`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run main-app.py --server.port=$PORT --server.address=0.0.0.0`
3. **Deploy**: Click "Create Web Service"

4. **Your demo will be live at**: `https://agent-squad-mvp.onrender.com`

---

## **OPTION 4: Docker (LOCAL NETWORK DEMO)**

**⏱️ Time**: 1 minute | **💰 Cost**: FREE | **🎯 Best for**: Local presentations

```bash
cd /Users/applepc/Documents/POc/agent-squad-mvp
docker build -t agent-squad-mvp .
docker run -p 8501:8501 agent-squad-mvp
```

**Access at**: `http://localhost:8501` or `http://YOUR_IP:8501`

---

## 🎯 **WHICH OPTION TO CHOOSE?**

| Platform | Best For | Time | Cost | URL |
|----------|----------|------|------|-----|
| **Streamlit Cloud** | Quick demos, sharing | 2 min | FREE | `*.streamlit.app` |
| **Railway** | Production demos | 5 min | $5/mo | `*.railway.app` |
| **Render** | Portfolio, sleep OK | 3 min | FREE | `*.onrender.com` |
| **Docker** | Local presentations | 1 min | FREE | `localhost:8501` |

## 🔗 **IMMEDIATE ACTION ITEMS**

1. **For quick demo**: Use Streamlit Cloud (Option 1)
2. **For professional demo**: Use Railway (Option 2)  
3. **For local demo**: Use Docker (Option 4)

**All deployment files are ready to go!** 🎉
