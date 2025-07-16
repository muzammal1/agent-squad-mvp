#!/usr/bin/env python3

import subprocess
import sys
import os

def main():
    # Change to the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("🚀 Starting Agent Squad MVP...")
    print("📁 Working directory:", script_dir)
    
    # Try to install requirements if venv doesn't exist
    venv_dirs = ['venv2', 'venv']
    python_executable = None
    
    for venv_dir in venv_dirs:
        if os.path.exists(venv_dir):
            # Try different Python executable names
            python_paths = [
                os.path.join(venv_dir, 'bin', 'python'),
                os.path.join(venv_dir, 'bin', 'python3'),
                os.path.join(venv_dir, 'bin', 'python3.13'),
            ]
            
            for python_path in python_paths:
                if os.path.exists(python_path):
                    python_executable = python_path
                    print(f"✅ Found Python at: {python_executable}")
                    break
            
            if python_executable:
                break
    
    if not python_executable:
        print("❌ No virtual environment found. Creating one...")
        # Create virtual environment
        subprocess.run([sys.executable, '-m', 'venv', 'venv3'], check=True)
        
        # Install requirements
        pip_path = os.path.join('venv3', 'bin', 'pip')
        if os.path.exists(pip_path):
            subprocess.run([pip_path, 'install', 'streamlit', 'python-dotenv', 'agent-squad'], check=True)
            python_executable = os.path.join('venv3', 'bin', 'python')
        else:
            print("❌ Failed to create virtual environment")
            return
    
    # Test imports
    try:
        result = subprocess.run([
            python_executable, '-c', 
            'import streamlit; import agent_squad; print("✅ All imports successful")'
        ], capture_output=True, text=True, check=True)
        print(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print(f"❌ Import test failed: {e}")
        print("Installing missing packages...")
        pip_path = python_executable.replace('python', 'pip').replace('python3', 'pip3')
        subprocess.run([pip_path, 'install', 'streamlit', 'python-dotenv', 'agent-squad'], check=True)
    
    # Run streamlit
    print("🌐 Starting Streamlit server...")
    print("📱 Access the app at: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop")
    
    cmd = [python_executable, '-m', 'streamlit', 'run', 'main-app.py', '--server.port=8501']
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n👋 Shutting down Agent Squad MVP...")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running streamlit: {e}")
        print("💡 Try running manually with:")
        print(f"   {python_executable} -m streamlit run main-app.py")

if __name__ == '__main__':
    main()
