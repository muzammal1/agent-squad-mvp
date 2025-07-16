#!/bin/bash
export PATH="/Users/applepc/Documents/POc/agent-squad-mvp/venv2/bin:$PATH"
export VIRTUAL_ENV="/Users/applepc/Documents/POc/agent-squad-mvp/venv2"
cd /Users/applepc/Documents/POc/agent-squad-mvp
/Users/applepc/Documents/POc/agent-squad-mvp/venv2/bin/python3 -m streamlit run main-app.py --server.port 8501
