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
import socket
import uvicorn

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def launch_browser():
    time.sleep(1.2)
    try:
        webbrowser.open("http://localhost:8001")
    except Exception:
        pass

if __name__ == "__main__":
    local_ip = get_local_ip()
    print("==================================================================")
    print("  📱 TRAVORA Mobile 9:16 Studio — Dedicated Mobile Localhost")
    print("==================================================================")
    print(f"  • Localhost URL:    http://localhost:8001")
    print(f"  • Localhost IP:     http://127.0.0.1:8001")
    print(f"  • Physical Mobile:  http://{local_ip}:8001 (Scan QR code in Studio)")
    print(f"  • Viewport Format:  9:16 Aspect Ratio (iPhone / Galaxy / Pixel)")
    print(f"  • Main Web Portal:  http://localhost:8000")
    print("==================================================================")
    print("  Starting Uvicorn server on port 8001 (host 0.0.0.0)...")
    print("==================================================================")
    threading.Thread(target=launch_browser, daemon=True).start()
    uvicorn.run("backend.mobile_server:mobile_app", host="0.0.0.0", port=8001, reload=True)
