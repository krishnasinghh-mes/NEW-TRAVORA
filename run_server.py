import os
import sys

# Ensure UTF-8 stdout on Windows
sys.stdout.reconfigure(encoding='utf-8')

# Ensure root directory is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import threading
import time
import webbrowser
import uvicorn

def launch_browser():
    time.sleep(1.2)
    try:
        webbrowser.open("http://127.0.0.1:8000")
    except Exception:
        pass

if __name__ == "__main__":
    print("==================================================================")
    print("  Starting TRAVORA -- AI-Powered Dynamic Tour Platform")
    print("  URL: http://127.0.0.1:8000")
    print("  API Docs: http://127.0.0.1:8000/docs")
    print("  Tagline: Plan Freely. Travel Personally. Adapt Instantly.")
    print("==================================================================")
    threading.Thread(target=launch_browser, daemon=True).start()
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
