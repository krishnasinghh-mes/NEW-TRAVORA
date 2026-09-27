# 🚀 TRAVORA Deployment Guide: GitHub Pages & Render.com

This repository is fully configured to be hosted on **GitHub Pages** (static desktop frontend) and/or deployed to **Render.com** (full-stack FastAPI Python server + SQLite).

---

## Option 1: Host on GitHub Pages (Instant Free Frontend)

GitHub Pages hosts the static frontend and renders the **complete TRAVORA Desktop View** directly in the browser with full interactive capabilities (802 Indian districts, AI trip planner, dynamic itineraries, flight & hotel search, live radar, and digital twin).

### Step 1: Create a GitHub Repository
1. Go to [github.com/new](https://github.com/new).
2. Name your repository (e.g. `TRAVORA` or `travora-travel`).
3. Set visibility to **Public** (required for free GitHub Pages).
4. Click **Create repository**.

### Step 2: Push Your Code to GitHub
#### Using GitHub Desktop (Easiest for Windows):
1. Open [GitHub Desktop](https://desktop.github.com/).
2. Click **File** -> **Add Local Repository...**
3. Select this folder: `c:\Users\Swati\Downloads\TRAVORA-20260926T054032Z-1-001\TRAVORA`.
4. Click **Publish repository** to push it to your GitHub account.

#### Or Using Command Line / Git CLI:
```bash
git init
git add .
git commit -m "Initial commit: TRAVORA AI dynamic tour platform with Desktop & 9:16 Mobile view"
git branch -M main
git remote add origin https://github.com/<YOUR_USERNAME>/<YOUR_REPO_NAME>.git
git push -u origin main
```

### Step 3: Enable GitHub Pages
1. In your GitHub repository, click on **Settings** (top tab).
2. On the left sidebar, click on **Pages**.
3. Under **Build and deployment** -> **Source**:
   - Choose **GitHub Actions** (recommended: uses the included `.github/workflows/deploy.yml` to automatically build and deploy every push).
   - *Or* choose **Deploy from a branch** -> select `main` branch -> folder `/ (root)` -> click **Save**.
4. Within 1–2 minutes, your website is live at:
   ```
   https://<YOUR_USERNAME>.github.io/<YOUR_REPO_NAME>/
   ```
5. Visiting this link immediately **renders the full TRAVORA Desktop View**!

---

## Option 2: Deploy on Render.com (Full-Stack Python Backend)

If you want the live Python FastAPI backend, SQLite database mutations, and dynamic background worker running 24/7 in the cloud:

### Step 1: Sign up on Render
1. Go to [render.com](https://render.com/) and sign in using your GitHub account.

### Step 2: Create a New Web Service
1. In Render Dashboard, click **New +** -> **Web Service**.
2. Select **Build and deploy from a Git repository**.
3. Connect your TRAVORA GitHub repository.

### Step 3: Configure Settings (Pre-configured via `render.yaml`)
Render will auto-detect the configuration, or you can verify:
- **Name**: `travora`
- **Region**: Oregon (US West) or Frankfurt
- **Branch**: `main`
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
- **Plan Type**: `Free`

### Step 4: Deploy
Click **Create Web Service**. Render will install dependencies and launch your application. Your live URL will be:
```
https://travora.onrender.com
```

---

## 📱 Desktop vs Mobile 9:16 on GitHub & Render

- **Desktop View**: Navigating to `https://<YOUR_USERNAME>.github.io/<YOUR_REPO_NAME>/` or `https://travora.onrender.com/` opens the **Desktop Portal**.
- **Mobile 9:16 Studio**: Navigating to `https://<YOUR_USERNAME>.github.io/<YOUR_REPO_NAME>/static/mobile.html` or `https://travora.onrender.com/mobile` opens the **9:16 Mobile View Studio**.
- **Local Testing**:
  - Run [`start_server.bat`](./start_server.bat) for desktop on `http://localhost:8000`.
  - Run [`start_mobile_server.bat`](./start_mobile_server.bat) for 9:16 mobile on `http://localhost:8001`.
