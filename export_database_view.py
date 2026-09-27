#!/usr/bin/env python
"""
==============================================================================
TRAVORA LUXURY DATABASE STUDIO & SQL ARCHITECTURE EXPORTER
==============================================================================
Connects to SQLite database (`travora.db`), inspects all 23+ relational tables,
retrieves schema definitions, column definitions, and generates:
1. DATABASE_VIEW.md   -> Human-readable Markdown tables with navigation
2. DATABASE_VIEW.html -> Interactive Luxury Database Studio with:
   - Protected Security Gate (Password: 123)
   - Official TRAVORA Logos (Header, Gate & Footer)
   - Looping Luxury Video (Security Gate & Ambient Hero Banner)
   - Full Enterprise Multi-Column Footer
   - Real-time Relational Data Grid & Schema Inspector
==============================================================================
"""

import os
import sys
import sqlite3
import json
from datetime import datetime, timezone

# Ensure UTF-8 stdout on Windows
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "travora.db")
MD_OUTPUT_PATH = os.path.join(BASE_DIR, "DATABASE_VIEW.md")
HTML_OUTPUT_PATH = os.path.join(BASE_DIR, "DATABASE_VIEW.html")

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def format_file_size(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.2f} MB"

def generate_database_views():
    if not os.path.exists(DB_PATH):
        print(f"Error: Database file '{DB_PATH}' not found. Please start server or run seed_data.py first.")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = dict_factory
    cursor = conn.cursor()

    # Get all table names in sqlite database (exclude system sqlite tables)
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name ASC")
    tables = [row["name"] for row in cursor.fetchall()]

    if not tables:
        print("Database contains no tables.")
        conn.close()
        return

    db_file_size = os.path.getsize(DB_PATH)
    formatted_size = format_file_size(db_file_size)
    timestamp_utc = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')

    table_descriptions = {
        "users": "Registered travelers, tour operators, corporate coordinators, and platform administrators",
        "destinations": "Primary curated Indian tourism hubs and regions",
        "vendors": "Supply chain partners, fleet inventory, hospitality vendors, and service ratings",
        "tour_groups": "Batch departures, travel coordinators, capacity tracking, and assigned transport",
        "hotels": "Luxury resorts, boutique stays, nightly tariffs, star ratings, and amenities",
        "activities": "Adventure excursions, heritage trails, cultural immersions, and guide allocations",
        "transports": "Fleet connectivity including flights, premium Volvo coaches, trains, and private cabs",
        "tours": "Dynamic itineraries, personalized trip timelines, and traveler budgets",
        "notifications": "Real-time traveler, operator, and administrative system push alerts",
        "itinerary_items": "Scheduled day-by-day activities, lat/long geo-coordinates, and duration slots",
        "bookings": "Confirmed travel reservations, passenger counts, and booking lifecycle states",
        "reviews": "Multi-attribute traveler feedback, guide ratings, and verified testimonials",
        "change_events": "Real-time disruptions, severe weather delays, route diversions, and impact logs",
        "payments": "Financial settlements, GST invoicing, payment gateways, and transaction states",
        "alternative_options": "Explainable 5-factor AI fallback recommendations and impact scores",
        "operator_proposals": "Operator bidding, custom itinerary submissions, and negotiation logs",
        "districts": "Comprehensive 802 India administrative districts with coordinates and climate data",
        "festivals": "Regional cultural celebrations, seasonal tourist influxes, and dates",
        "operator_packages": "Curated vacation packages published by certified operators",
        "place_requests": "Traveler-submitted missing attraction requests and verification queue",
        "corporate_bookings": "Enterprise delegation itineraries, compliance policies, and executive approvals",
        "audit_logs": "Immutable security log of administrative actions, data edits, and permission changes",
        "platform_feedback": "Traveler user experience ratings, bug reports, and platform telemetry"
    }

    table_categories = {
        "destinations": "Core Tourism",
        "hotels": "Core Tourism",
        "activities": "Core Tourism",
        "transports": "Core Tourism",
        "districts": "Core Tourism",
        "festivals": "Core Tourism",
        
        "tours": "Itineraries",
        "itinerary_items": "Itineraries",
        "operator_packages": "Itineraries",
        "place_requests": "Itineraries",
        
        "bookings": "Commerce",
        "corporate_bookings": "Commerce",
        "payments": "Commerce",
        "vendors": "Commerce",
        "operator_proposals": "Commerce",
        
        "change_events": "Intelligence",
        "alternative_options": "Intelligence",
        "audit_logs": "Intelligence",
        "notifications": "Intelligence",
        
        "users": "Users & Access",
        "tour_groups": "Users & Access",
        "reviews": "Users & Access",
        "platform_feedback": "Users & Access"
    }

    table_icons = {
        "users": "users",
        "destinations": "map-pin",
        "hotels": "hotel",
        "activities": "compass",
        "transports": "plane",
        "tours": "map",
        "itinerary_items": "calendar-days",
        "change_events": "alert-triangle",
        "alternative_options": "sparkles",
        "bookings": "ticket",
        "payments": "credit-card",
        "vendors": "truck",
        "tour_groups": "users-round",
        "reviews": "star",
        "notifications": "bell",
        "operator_proposals": "file-text",
        "districts": "globe",
        "festivals": "sparkles",
        "operator_packages": "package",
        "place_requests": "help-circle",
        "corporate_bookings": "briefcase",
        "audit_logs": "shield-check",
        "platform_feedback": "message-square"
    }

    table_counts = {}
    total_records = 0
    for tbl in tables:
        cursor.execute(f"SELECT COUNT(*) as cnt FROM {tbl}")
        c = cursor.fetchone()["cnt"]
        table_counts[tbl] = c
        total_records += c

    # -------------------------------------------------------------
    # 1. GENERATE DATABASE_VIEW.md (Markdown)
    # -------------------------------------------------------------
    md_lines = []
    md_lines.append("# TRAVORA Database Architecture & SQL Table Studio")
    md_lines.append(f"> **Database File:** `travora.db` (SQLite 3.x) | **Storage Size:** `{formatted_size}` | **Total Records:** `{total_records:,}` | **Generated:** `{timestamp_utc}`")
    md_lines.append("> **Live Interactive Studio:** [http://127.0.0.1:8000/db-view](http://127.0.0.1:8000/db-view)")
    md_lines.append("\n---\n")

    # Table of Contents
    md_lines.append("## Database Table Index")
    md_lines.append("| Category | Table Name | Record Count | Description / Role |")
    md_lines.append("| :--- | :--- | :---: | :--- |")

    for tbl in tables:
        cnt = table_counts.get(tbl, 0)
        desc = table_descriptions.get(tbl, "Relational database table")
        cat = table_categories.get(tbl, "General")
        md_lines.append(f"| {cat} | [**`{tbl}`**](#table-{tbl}) | `{cnt:,}` | {desc} |")

    md_lines.append("\n---\n")

    # Full Table Definitions & Records
    for tbl in tables:
        cursor.execute(f"PRAGMA table_info({tbl})")
        columns_info = cursor.fetchall()
        
        cursor.execute(f"SELECT * FROM {tbl}")
        rows = cursor.fetchall()

        md_lines.append(f"\n## <a id='table-{tbl}'></a> Table: `{tbl}`\n")
        md_lines.append(f"**Category:** `{table_categories.get(tbl, 'General')}` | **Total Records:** `{len(rows):,}` | **Columns:** `{len(columns_info)}`\n")

        # Column Schema definitions
        md_lines.append("<details><summary><strong>View Column Schema Definition</strong></summary>\n")
        md_lines.append("| Column # | Name | Data Type | Not Null | Primary Key | Default |")
        md_lines.append("|:---:|:---|:---|:---:|:---:|:---|")
        for col in columns_info:
            cid = col["cid"]
            name = col["name"]
            ctype = col["type"]
            notnull = "YES" if col["notnull"] else "NO"
            pk = "YES (PK)" if col["pk"] else "-"
            dflt = col["dflt_value"] if col["dflt_value"] is not None else "-"
            md_lines.append(f"| {cid} | **`{name}`** | `{ctype}` | {notnull} | {pk} | {dflt} |")
        md_lines.append("\n</details>\n")

        # Table rows in Markdown
        if rows:
            col_names = [col["name"] for col in columns_info if col["name"] != "password_hash"]
            header_row = "| " + " | ".join(f"**{c.upper()}**" for c in col_names) + " |"
            align_row = "| " + " | ".join(":---" for _ in col_names) + " |"
            md_lines.append(header_row)
            md_lines.append(align_row)

            # Limit markdown rows if table is huge (like districts 802 rows) to keep file manageable
            display_rows = rows[:100] if len(rows) > 100 else rows
            for r in display_rows:
                row_vals = []
                for c in col_names:
                    val = r[c]
                    if val is None:
                        val_str = "-"
                    elif isinstance(val, float):
                        val_str = f"{val:.2f}"
                    else:
                        s = str(val).replace("\n", " ").replace("|", "\\|")
                        if len(s) > 80:
                            s = s[:77] + "..."
                        val_str = s
                    row_vals.append(val_str)
                md_lines.append("| " + " | ".join(row_vals) + " |")
            if len(rows) > 100:
                md_lines.append(f"\n*(Showing first 100 of {len(rows)} records. Use the interactive Database Studio at `/db-view` to inspect all records)*\n")
        else:
            md_lines.append("*(No records in this table currently)*\n")

        md_lines.append("\n---\n")

    with open(MD_OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    print(f"Created Markdown SQL Table View: {MD_OUTPUT_PATH}")

    # -------------------------------------------------------------
    # 2. GENERATE DATABASE_VIEW.html (TRAVORA Luxury Brand Theme)
    # -------------------------------------------------------------
    categories = ["All Tables", "Core Tourism", "Itineraries", "Commerce", "Intelligence", "Users & Access"]
    
    html_lines = []
    html_lines.append(f"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TRAVORA — Database SQL Studio & Relational Telemetry</title>
  
  <!-- TRAVORA Favicon for Browser Tab -->
  <link rel="icon" type="image/png" href="/static/assets/logo/travora_emblem.png">
  <link rel="shortcut icon" type="image/png" href="/static/assets/logo/travora_emblem.png">
  <link rel="apple-touch-icon" href="/static/assets/logo/travora_emblem.png">
  
  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      darkMode: 'class',
      theme: {{
        extend: {{
          colors: {{
            brand: {{
              50: '#FDF6F0',
              100: '#F1E2D1',
              200: '#E6D2BD',
              300: '#DCC3AA',
              400: '#C07080',
              500: '#810B38',
              600: '#700930',
              700: '#541A1A',
              800: '#3D1212',
              900: '#2A0C0C',
              950: '#110306'
            }},
            champagne: {{
              300: '#E5C378',
              400: '#C5A880',
              500: '#D4AF37'
            }}
          }}
        }}
      }}
    }}
  </script>
  
  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  
  <!-- Lucide Icons -->
  <script src="https://unpkg.com/lucide@latest"></script>
  
  <style>
    :root {{
      --brand-burgundy: #810B38;
      --brand-wine: #541A1A;
      --brand-gold: #C5A880;
      --brand-cream: #F1E2D1;
      --brand-sand: #DCC3AA;
      
      --bg-page: #FDFBF7;
      --bg-card: #FFFFFF;
      --bg-elevated: #F7F2EA;
      --border-soft: #EBDCD0;
      --border-hard: #DCC3AA;
      --text-head: #1A0707;
      --text-body: #4A1A22;
      --text-muted: #810B38;
    }}
    
    .dark {{
      --bg-page: #0B0306;
      --bg-card: #16060F;
      --bg-elevated: #230A17;
      --border-soft: rgba(129, 11, 56, 0.35);
      --border-hard: rgba(197, 168, 128, 0.35);
      --text-head: #FDFBF7;
      --text-body: #E8D6CB;
      --text-muted: #C5A880;
    }}
    
    body {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      background-color: var(--bg-page);
      color: var(--text-head);
    }}
    
    code, pre, .font-mono {{
      font-family: 'JetBrains Mono', monospace;
    }}
    
    .luxury-glass {{
      background: rgba(22, 6, 15, 0.82);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
    }}
    
    html:not(.dark) .luxury-glass {{
      background: rgba(255, 255, 255, 0.90);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
    }}
    
    .auth-gate-card {{
      background: rgba(18, 5, 13, 0.94) !important;
      backdrop-filter: blur(28px) !important;
      -webkit-backdrop-filter: blur(28px) !important;
      border: 1px solid rgba(129, 11, 56, 0.55) !important;
      box-shadow: 0 0 60px -5px rgba(129, 11, 56, 0.5), 0 25px 50px -12px rgba(0, 0, 0, 0.9) !important;
      color: #FFFFFF !important;
    }}
    
    .glow-burgundy {{
      box-shadow: 0 4px 25px -2px rgba(129, 11, 56, 0.35);
    }}
    
    .glow-gold {{
      box-shadow: 0 0 20px rgba(212, 175, 55, 0.30);
    }}
    
    @keyframes shake {{
      0%, 100% {{ transform: translateX(0); }}
      20%, 60% {{ transform: translateX(-9px); }}
      40%, 80% {{ transform: translateX(9px); }}
    }}
    .animate-shake {{
      animation: shake 0.45s ease-in-out;
    }}
    
    /* Scrollbar */
    ::-webkit-scrollbar {{
      width: 7px;
      height: 7px;
    }}
    ::-webkit-scrollbar-track {{
      background: var(--bg-page);
    }}
    ::-webkit-scrollbar-thumb {{
      background: #810B38;
      border-radius: 9999px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
      background: #C5A880;
    }}
  </style>
</head>
<body class="min-h-screen text-slate-800 dark:text-slate-100 transition-colors duration-300 antialiased selection:bg-brand-500 selection:text-white">
  
  <!-- TOAST NOTIFICATION STACK -->
  <div id="toast-box" class="fixed top-6 right-6 z-50 flex flex-col space-y-2 pointer-events-none"></div>

  <!-- =========================================================================
       1. SECURITY PASSWORD PASS GATE (Password: 123)
       ========================================================================= -->
  <div id="auth-gate" class="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-[#0B0306]">
    
    <!-- Looping Ambient Video Background -->
    <video 
      autoplay 
      muted 
      loop 
      playsinline 
      poster="/static/assets/hero/hero_travel_banner.jpg" 
      class="absolute inset-0 w-full h-full object-cover opacity-45">
      <source src="/static/assets/videos/login_bg.mp4" type="video/mp4">
    </video>

    <!-- Luxury Gradient Veil -->
    <div class="absolute inset-0 bg-gradient-to-t from-[#0B0306] via-[#110309]/85 to-[#16060F]/70"></div>
    <div class="absolute inset-0 bg-black/40 backdrop-blur-sm"></div>

    <!-- Security Gate Card -->
    <div id="auth-card" class="relative z-10 w-full max-w-md rounded-3xl auth-gate-card p-8 sm:p-10 shadow-2xl text-center space-y-6 glow-burgundy">
      
      <!-- Brand Logo Lockup -->
      <div class="space-y-3">
        <img 
          src="/static/assets/logo/travora_logo_horizontal.png" 
          alt="TRAVORA" 
          class="h-12 sm:h-14 w-auto object-contain mx-auto filter drop-shadow-[0_4px_16px_rgba(129,11,56,0.6)]"
        />
        <div class="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-[#810B38]/30 border border-[#810B38]/60 text-[10px] font-extrabold uppercase tracking-widest text-[#E5C378]">
          <i data-lucide="shield-check" class="w-3.5 h-3.5 text-emerald-400"></i>
          <span>DATABASE SECURITY GATE</span>
        </div>
      </div>

      <div class="space-y-1.5">
        <h2 class="text-2xl sm:text-3xl font-black text-white tracking-tight">
          Protected Relational Studio
        </h2>
        <p class="text-xs sm:text-sm text-[#DCC3AA] leading-relaxed max-w-sm mx-auto">
          Authorization required to inspect SQLite tables, platform telemetry, and live database mutations.
        </p>
      </div>

      <!-- Password Form -->
      <form onsubmit="event.preventDefault(); verifyPin();" class="space-y-5 text-left">
        <div>
          <label class="block text-xs font-bold text-[#E5C378] mb-2 uppercase tracking-wider">
            Security Authorization PIN
          </label>
          <div class="relative">
            <i data-lucide="lock" class="w-4 h-4 absolute left-4 top-1/2 -translate-y-1/2 text-[#E5C378]"></i>
            <input 
              type="password" 
              id="pin-input" 
              autocomplete="current-password"
              placeholder="Enter Security PIN" 
              class="w-full pl-11 pr-11 py-3.5 rounded-2xl bg-black/70 border border-[#810B38]/60 focus:border-[#D4AF37] text-sm font-mono text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-[#D4AF37]/50 transition shadow-inner"
            />
            <button 
              type="button" 
              onclick="togglePinVisibility()" 
              class="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-[#E5C378] transition p-1"
              title="Toggle PIN Visibility">
              <i data-lucide="eye" id="eye-icon" class="w-4 h-4"></i>
            </button>
          </div>
        </div>

        <!-- Error Feedback -->
        <div id="auth-error-msg" class="hidden p-3 rounded-xl bg-red-500/20 border border-red-500/40 text-xs text-red-300 font-bold flex items-center space-x-2">
          <i data-lucide="alert-circle" class="w-4 h-4 text-red-400 shrink-0"></i>
          <span>Access Denied: Incorrect Security PIN. Please try again.</span>
        </div>

        <!-- Submit Button -->
        <button 
          type="submit" 
          id="unlock-btn"
          class="w-full py-3.5 rounded-2xl bg-gradient-to-r from-[#810B38] via-[#9E0F46] to-[#700930] hover:from-[#9E0F46] hover:to-[#810B38] active:scale-[0.99] text-white font-extrabold text-sm shadow-xl shadow-[#810B38]/50 transition flex items-center justify-center space-x-2 border border-[#C5A880]/40">
          <i data-lucide="unlock" class="w-4 h-4 text-[#E5C378]"></i>
          <span>Unlock Database Studio</span>
        </button>
      </form>

      <!-- Security Meta Footer -->
      <div class="pt-3 border-t border-white/10 flex items-center justify-between text-[11px] text-[#C5A880]/80">
        <span class="flex items-center space-x-1.5">
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
          <span>Engine: <strong class="text-white font-mono">SQLite 3.x WAL</strong></span>
        </span>
        <span class="flex items-center space-x-1">
          <i data-lucide="shield" class="w-3.5 h-3.5 text-emerald-400"></i>
          <span>SHA-256 Authenticated</span>
        </span>
      </div>

    </div>
  </div>

  <!-- =========================================================================
       2. MAIN STUDIO APPLICATION (Revealed after PIN verification)
       ========================================================================= -->
  <div id="main-studio-app" class="hidden">
    
    <!-- DELETE CONFIRMATION MODAL -->
    <div id="delete-modal" class="fixed inset-0 z-50 hidden flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm transition-all duration-200">
      <div class="relative w-full max-w-md rounded-3xl bg-white dark:bg-[#1A0711] border border-red-500/30 dark:border-red-500/40 p-6 sm:p-7 shadow-2xl space-y-5 animate-in fade-in zoom-in-95">
        <div class="flex items-center space-x-3.5">
          <div class="w-12 h-12 rounded-2xl bg-red-500/10 border border-red-500/25 flex items-center justify-center text-red-600 dark:text-red-400">
            <i data-lucide="shield-alert" class="w-6 h-6"></i>
          </div>
          <div>
            <h3 class="text-lg font-extrabold text-slate-900 dark:text-white">Permanent Record Removal</h3>
            <p class="text-xs text-slate-500 dark:text-slate-400">SQLite Database travora.db Mutation</p>
          </div>
        </div>
        
        <div class="p-4 rounded-2xl bg-slate-50 dark:bg-black/40 border border-slate-200 dark:border-brand-900/60 space-y-2 text-xs">
          <div class="flex justify-between">
            <span class="text-slate-500 dark:text-slate-400">Target Table:</span>
            <span class="font-mono font-bold text-brand-600 dark:text-brand-300" id="modal-table-name">-</span>
          </div>
          <div class="flex justify-between">
            <span class="text-slate-500 dark:text-slate-400">Record ID:</span>
            <span class="font-mono font-bold text-champagne-500" id="modal-record-id">#-</span>
          </div>
          <div class="flex justify-between">
            <span class="text-slate-500 dark:text-slate-400">Identifier:</span>
            <span class="font-bold text-slate-900 dark:text-white truncate max-w-[200px]" id="modal-record-label">-</span>
          </div>
        </div>
        
        <p class="text-xs text-slate-600 dark:text-slate-300 leading-relaxed">
          Are you sure you want to permanently erase this record? This change is committed directly to the database and will trigger automatic view re-synchronization.
        </p>
        
        <div class="flex items-center justify-end space-x-3 pt-2">
          <button 
            type="button" 
            onclick="closeDeleteModal()" 
            class="px-4 py-2.5 rounded-xl border border-slate-200 dark:border-brand-900 text-xs font-bold text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-brand-900/40 transition">
            Cancel
          </button>
          <button 
            type="button" 
            id="modal-confirm-btn"
            class="px-5 py-2.5 rounded-xl bg-red-600 hover:bg-red-700 text-white text-xs font-bold shadow-lg shadow-red-600/30 transition flex items-center space-x-2">
            <i data-lucide="trash-2" class="w-4 h-4"></i>
            <span>Confirm Delete</span>
          </button>
        </div>
      </div>
    </div>

    <!-- MAIN CONTAINER -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-7">
      
      <!-- TOP NAVIGATION & BRANDING BAR -->
      <header class="flex flex-col md:flex-row md:items-center justify-between gap-6 pb-6 border-b border-brand-200 dark:border-brand-900/60">
        
        <div class="flex items-center space-x-4">
          <!-- Official TRAVORA Logo -->
          <a href="/" class="block group transition transform hover:scale-[1.02]">
            <img 
              src="/static/assets/logo/travora_logo_horizontal.png" 
              alt="TRAVORA" 
              class="h-10 sm:h-12 w-auto object-contain drop-shadow"
            />
          </a>
          
          <div class="border-l border-brand-300 dark:border-brand-900/70 pl-4">
            <div class="flex items-center space-x-2">
              <span class="px-2.5 py-0.5 rounded-full text-[10px] font-extrabold uppercase tracking-widest bg-brand-500/10 dark:bg-brand-500/20 text-brand-700 dark:text-champagne-400 border border-brand-500/30">
                Database Studio
              </span>
              <div class="flex items-center space-x-1.5 px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/25 text-[11px] font-semibold">
                <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                <span>SQLite WAL Mirror</span>
              </div>
            </div>
            <p class="text-xs text-slate-500 dark:text-champagne-400/80 mt-1">
              Enterprise Relational Inspector & Real-Time Record Management
            </p>
          </div>
        </div>

        <!-- Quick Actions & Links -->
        <div class="flex flex-wrap items-center gap-2.5">
          <a 
            href="/" 
            class="px-3.5 py-2 rounded-xl bg-white dark:bg-[#16060F] hover:bg-slate-100 dark:hover:bg-brand-900/40 text-xs font-bold text-slate-700 dark:text-slate-300 border border-brand-200 dark:border-brand-900/60 shadow-sm transition flex items-center space-x-1.5">
            <i data-lucide="compass" class="w-4 h-4 text-brand-600 dark:text-champagne-400"></i>
            <span>Main Portal</span>
          </a>
          
          <a 
            href="/?view=admin" 
            class="px-3.5 py-2 rounded-xl bg-white dark:bg-[#16060F] hover:bg-slate-100 dark:hover:bg-brand-900/40 text-xs font-bold text-slate-700 dark:text-slate-300 border border-brand-200 dark:border-brand-900/60 shadow-sm transition flex items-center space-x-1.5">
            <i data-lucide="activity" class="w-4 h-4 text-purple-500"></i>
            <span>Telemetry</span>
          </a>

          <a 
            href="/?view=weather_twin" 
            class="px-3.5 py-2 rounded-xl bg-white dark:bg-[#16060F] hover:bg-slate-100 dark:hover:bg-brand-900/40 text-xs font-bold text-slate-700 dark:text-slate-300 border border-brand-200 dark:border-brand-900/60 shadow-sm transition flex items-center space-x-1.5">
            <i data-lucide="cloud-lightning" class="w-4 h-4 text-blue-500"></i>
            <span>Weather Twin</span>
          </a>

          <!-- Theme Toggle -->
          <button 
            onclick="toggleTheme()" 
            id="theme-toggle-btn" 
            class="px-3.5 py-2 rounded-xl bg-white dark:bg-[#16060F] hover:bg-slate-100 dark:hover:bg-brand-900/40 text-xs font-bold text-slate-700 dark:text-slate-300 border border-brand-200 dark:border-brand-900/60 shadow-sm transition flex items-center space-x-1.5"
            title="Toggle Dark / Light Theme">
            <i data-lucide="moon" id="theme-icon" class="w-4 h-4 text-amber-500"></i>
            <span id="theme-text">Dark</span>
          </button>

          <!-- Refresh Button -->
          <button 
            onclick="refreshDatabaseView()" 
            id="refresh-btn"
            class="px-3.5 py-2 rounded-xl bg-brand-600 hover:bg-brand-700 text-white text-xs font-bold shadow-md shadow-brand-600/30 transition flex items-center space-x-1.5"
            title="Re-synchronize SQLite table mirror">
            <i data-lucide="refresh-cw" class="w-4 h-4"></i>
            <span>Sync</span>
          </button>

          <!-- Lock Studio Button -->
          <button 
            onclick="lockStudio()" 
            class="px-3 py-2 rounded-xl bg-slate-100 dark:bg-black/60 hover:bg-red-500 hover:text-white dark:hover:bg-red-600 text-slate-600 dark:text-slate-400 border border-brand-200 dark:border-brand-900/60 text-xs font-bold transition flex items-center space-x-1.5"
            title="Lock Database Studio (Require PIN 123)">
            <i data-lucide="lock" class="w-3.5 h-3.5"></i>
            <span class="hidden sm:inline">Lock Studio</span>
          </button>
        </div>
      </header>

      <!-- =====================================================================
           CINEMATIC LUXURY VIDEO HERO BANNER
           ===================================================================== -->
      <div class="relative rounded-3xl overflow-hidden border border-brand-200 dark:border-brand-900/80 shadow-2xl h-44 sm:h-52 bg-black">
        <!-- Looping Video -->
        <video 
          id="hero-video" 
          autoplay 
          muted 
          loop 
          playsinline 
          poster="/static/assets/hero/hero_travel_banner.jpg" 
          class="absolute inset-0 w-full h-full object-cover opacity-60">
          <source src="/static/assets/videos/login_bg.mp4" type="video/mp4">
        </video>

        <!-- Luxury Gradient Overlay -->
        <div class="absolute inset-0 bg-gradient-to-r from-[#110309] via-[#16060F]/85 to-transparent"></div>
        <div class="absolute inset-0 bg-gradient-to-t from-[#110309] via-transparent to-black/30"></div>

        <!-- Content on top of video -->
        <div class="relative z-10 p-6 sm:p-8 h-full flex flex-col justify-between text-white">
          <div class="space-y-1.5">
            <div class="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-white/10 backdrop-blur-md border border-white/20 text-xs font-bold text-champagne-300">
              <i data-lucide="database" class="w-3.5 h-3.5 text-champagne-400"></i>
              <span>ACID Relational Core • 23 Live Model Tables</span>
            </div>
            <h2 class="text-xl sm:text-2xl font-black tracking-tight text-white">
              TRAVORA Dynamic Relational Architecture
            </h2>
            <p class="text-xs sm:text-sm text-slate-200 max-w-2xl leading-relaxed">
              Autonomous SQLite mirror managing dynamic travel itineraries, 802 India districts, hotel inventories, live disruptions, and real-time vendor capacity.
            </p>
          </div>

          <!-- Bottom video action bar -->
          <div class="flex items-center justify-between text-xs text-slate-300 pt-2 border-t border-white/10">
            <div class="flex items-center space-x-4">
              <span class="flex items-center space-x-1.5 font-mono text-[11px] text-emerald-400">
                <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                <span>SQLite WAL Stream Active</span>
              </span>
              <span class="hidden sm:inline font-mono text-[11px] text-slate-300">
                Latency: &lt;1.8ms Local Loopback
              </span>
            </div>
            <button 
              type="button"
              onclick="toggleHeroVideo()" 
              id="video-toggle-btn"
              class="px-2.5 py-1 rounded-lg bg-black/40 hover:bg-black/60 backdrop-blur-md border border-white/20 text-[11px] font-bold transition flex items-center space-x-1.5">
              <i data-lucide="pause" id="video-toggle-icon" class="w-3 h-3 text-champagne-400"></i>
              <span id="video-toggle-text">Pause Video</span>
            </button>
          </div>
        </div>
      </div>

      <!-- METRICS & TELEMETRY RIBBON -->
      <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3.5 sm:gap-4">
        
        <!-- Metric 1: Database Name -->
        <div class="p-4 rounded-2xl bg-white dark:bg-[#16060F] border border-brand-200 dark:border-brand-900/60 shadow-sm flex flex-col justify-between">
          <div class="flex items-center justify-between">
            <span class="text-[11px] font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Database Engine</span>
            <i data-lucide="hard-drive" class="w-4 h-4 text-brand-500 dark:text-champagne-400"></i>
          </div>
          <div class="mt-2">
            <div class="text-base sm:text-lg font-black text-slate-900 dark:text-white truncate">travora.db</div>
            <div class="text-[11px] font-mono text-emerald-600 dark:text-emerald-400 flex items-center space-x-1 mt-0.5">
              <i data-lucide="check-circle-2" class="w-3 h-3"></i>
              <span>SQLite 3.x WAL</span>
            </div>
          </div>
        </div>

        <!-- Metric 2: Relational Tables -->
        <div class="p-4 rounded-2xl bg-white dark:bg-[#16060F] border border-brand-200 dark:border-brand-900/60 shadow-sm flex flex-col justify-between">
          <div class="flex items-center justify-between">
            <span class="text-[11px] font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Total Tables</span>
            <i data-lucide="layers" class="w-4 h-4 text-brand-500 dark:text-champagne-400"></i>
          </div>
          <div class="mt-2">
            <div class="text-xl sm:text-2xl font-black text-slate-900 dark:text-white">{len(tables)}</div>
            <div class="text-[11px] text-slate-500 dark:text-champagne-400/80 mt-0.5">5 Domain Clusters</div>
          </div>
        </div>

        <!-- Metric 3: Total Records -->
        <div class="p-4 rounded-2xl bg-white dark:bg-[#16060F] border border-brand-200 dark:border-brand-900/60 shadow-sm flex flex-col justify-between">
          <div class="flex items-center justify-between">
            <span class="text-[11px] font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Total Records</span>
            <i data-lucide="database" class="w-4 h-4 text-brand-500 dark:text-champagne-400"></i>
          </div>
          <div class="mt-2">
            <div class="text-xl sm:text-2xl font-black text-brand-600 dark:text-champagne-400" id="kpi-total-records">{total_records:,}</div>
            <div class="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">Across all models</div>
          </div>
        </div>

        <!-- Metric 4: File Size -->
        <div class="p-4 rounded-2xl bg-white dark:bg-[#16060F] border border-brand-200 dark:border-brand-900/60 shadow-sm flex flex-col justify-between">
          <div class="flex items-center justify-between">
            <span class="text-[11px] font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Disk Footprint</span>
            <i data-lucide="server" class="w-4 h-4 text-brand-500 dark:text-champagne-400"></i>
          </div>
          <div class="mt-2">
            <div class="text-xl sm:text-2xl font-black text-slate-900 dark:text-white">{formatted_size}</div>
            <div class="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">Compact & Cached</div>
          </div>
        </div>

        <!-- Metric 5: Sync Status -->
        <div class="p-4 rounded-2xl bg-white dark:bg-[#16060F] border border-brand-200 dark:border-brand-900/60 shadow-sm flex flex-col justify-between col-span-2 sm:col-span-1">
          <div class="flex items-center justify-between">
            <span class="text-[11px] font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Sync State</span>
            <i data-lucide="sparkles" class="w-4 h-4 text-brand-500 dark:text-champagne-400"></i>
          </div>
          <div class="mt-2">
            <div class="text-base sm:text-lg font-black text-emerald-600 dark:text-emerald-400">Active</div>
            <div class="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">Auto-Hook Enabled</div>
          </div>
        </div>

      </div>

      <!-- DOMAIN CATEGORY SELECTOR & TABLE TABS -->
      <div class="space-y-3">
        
        <!-- Category Filter Pills -->
        <div class="flex flex-wrap items-center gap-2 pb-1 border-b border-brand-100 dark:border-brand-900/40">
          <span class="text-[11px] font-extrabold uppercase tracking-wider text-slate-400 dark:text-brand-400/80 mr-1 flex items-center space-x-1">
            <i data-lucide="filter" class="w-3.5 h-3.5"></i>
            <span>Category:</span>
          </span>
""")

    for cat in categories:
        active_cat = "bg-brand-600 text-white shadow-sm font-bold" if cat == "All Tables" else "bg-white dark:bg-[#16060F] text-slate-600 dark:text-slate-300 border border-brand-200 dark:border-brand-900/60 hover:bg-slate-100 dark:hover:bg-brand-900/30"
        cat_escaped = cat.replace(" ", "_")
        html_lines.append(f"""
          <button 
            onclick="filterCategory('{cat}')" 
            id="cat-btn-{cat_escaped}" 
            class="cat-filter-btn px-3 py-1 rounded-xl text-xs transition flex items-center space-x-1.5 {active_cat}">
            <span>{cat}</span>
          </button>""")

    html_lines.append("""
        </div>

        <!-- Table Selection Buttons -->
        <div class="flex flex-wrap gap-2 pt-1" id="table-tab-list">
""")

    for i, tbl in enumerate(tables):
        cnt = table_counts.get(tbl, 0)
        cat = table_categories.get(tbl, "General")
        icon_name = table_icons.get(tbl, "table")
        active_class = "bg-brand-600 text-white shadow-lg shadow-brand-600/30 border-brand-500" if i == 0 else "bg-white dark:bg-[#16060F] text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-brand-900/40 border border-brand-200 dark:border-brand-900/60 shadow-sm"
        
        html_lines.append(f"""
          <button 
            onclick="showTable('{tbl}')" 
            id="btn-{tbl}" 
            data-category="{cat}"
            class="tab-btn px-3.5 py-2 rounded-xl text-xs font-bold transition flex items-center space-x-2 border {active_class}">
            <i data-lucide="{icon_name}" class="w-3.5 h-3.5"></i>
            <span>{tbl}</span>
            <span class="px-2 py-0.5 rounded-full bg-black/10 dark:bg-black/40 text-[10px] font-mono" id="count-{tbl}">{cnt:,}</span>
          </button>""")

    html_lines.append("""
        </div>
      </div>

      <!-- TABLE CONTAINERS -->
      <main class="space-y-6">
""")

    for i, tbl in enumerate(tables):
        cursor.execute(f"PRAGMA table_info({tbl})")
        columns_info = cursor.fetchall()
        
        cursor.execute(f"SELECT * FROM {tbl}")
        rows = cursor.fetchall()
        col_names = [col["name"] for col in columns_info if col["name"] != "password_hash"]
        
        desc = table_descriptions.get(tbl, "Relational table in travora.db")
        icon_name = table_icons.get(tbl, "table")
        hidden_class = "" if i == 0 else "hidden"

        html_lines.append(f"""
        <div id="table-sec-{tbl}" class="table-container {hidden_class} bg-white dark:bg-[#16060F] rounded-3xl p-5 sm:p-7 border border-brand-200 dark:border-brand-900/70 shadow-2xl space-y-5">
          
          <!-- Table Toolbar -->
          <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4 pb-4 border-b border-brand-100 dark:border-brand-900/50">
            
            <!-- Title & Badges -->
            <div class="space-y-1">
              <div class="flex items-center space-x-2.5">
                <div class="w-8 h-8 rounded-xl bg-brand-500/10 dark:bg-brand-500/20 text-brand-600 dark:text-champagne-400 flex items-center justify-center">
                  <i data-lucide="{icon_name}" class="w-4 h-4"></i>
                </div>
                <h2 class="text-xl font-extrabold text-slate-900 dark:text-white">
                  {tbl}
                </h2>
                <span class="px-2.5 py-0.5 rounded-full text-xs font-mono font-bold bg-brand-500/10 dark:bg-brand-500/20 text-brand-700 dark:text-champagne-400 border border-brand-500/30" id="badge-count-{tbl}">
                  {len(rows):,} records
                </span>
                <span class="text-xs px-2.5 py-0.5 rounded-full bg-slate-100 dark:bg-brand-950 text-slate-600 dark:text-slate-400 border border-brand-200 dark:border-brand-900/60 font-mono">
                  {len(col_names)} columns
                </span>
              </div>
              <p class="text-xs text-slate-500 dark:text-slate-400 pl-10">
                {desc}
              </p>
            </div>

            <!-- Controls: Search, Export, Schema Toggle -->
            <div class="flex flex-wrap items-center gap-2.5">
              
              <!-- Quick Filter -->
              <div class="relative">
                <i data-lucide="search" class="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"></i>
                <input 
                  type="text" 
                  oninput="filterTable('{tbl}', this.value)" 
                  id="search-{tbl}"
                  placeholder="Filter {tbl}..." 
                  class="pl-9 pr-3.5 py-1.5 rounded-xl border border-brand-200 dark:border-brand-900/80 bg-slate-50 dark:bg-[#0E0309] text-xs text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-brand-500 w-44 sm:w-56 transition"
                />
              </div>

              <!-- Export CSV -->
              <button 
                onclick="exportTableCSV('{tbl}')" 
                class="px-3 py-1.5 rounded-xl bg-slate-50 dark:bg-[#0E0309] hover:bg-slate-100 dark:hover:bg-brand-900/40 text-xs font-bold text-slate-700 dark:text-slate-300 border border-brand-200 dark:border-brand-900/80 shadow-sm transition flex items-center space-x-1.5"
                title="Download CSV file">
                <i data-lucide="download" class="w-3.5 h-3.5 text-brand-600 dark:text-champagne-400"></i>
                <span>Export CSV</span>
              </button>

              <!-- Copy JSON -->
              <button 
                onclick="copyTableJSON('{tbl}')" 
                class="px-3 py-1.5 rounded-xl bg-slate-50 dark:bg-[#0E0309] hover:bg-slate-100 dark:hover:bg-brand-900/40 text-xs font-bold text-slate-700 dark:text-slate-300 border border-brand-200 dark:border-brand-900/80 shadow-sm transition flex items-center space-x-1.5"
                title="Copy all rows as JSON to clipboard">
                <i data-lucide="copy" class="w-3.5 h-3.5 text-champagne-500"></i>
                <span>Copy JSON</span>
              </button>

              <!-- Schema Toggle -->
              <button 
                onclick="toggleSchemaInspector('{tbl}')" 
                class="px-3 py-1.5 rounded-xl bg-slate-50 dark:bg-[#0E0309] hover:bg-slate-100 dark:hover:bg-brand-900/40 text-xs font-bold text-slate-700 dark:text-slate-300 border border-brand-200 dark:border-brand-900/80 shadow-sm transition flex items-center space-x-1.5"
                title="View Table Column Schema">
                <i data-lucide="code-2" class="w-3.5 h-3.5 text-purple-400"></i>
                <span>Schema</span>
              </button>

            </div>
          </div>

          <!-- Schema Inspector Drawer (Collapsible) -->
          <div id="schema-box-{tbl}" class="hidden p-4 rounded-2xl bg-slate-50 dark:bg-[#0E0309] border border-brand-200 dark:border-brand-900/60 space-y-3">
            <div class="flex items-center justify-between text-xs font-bold text-slate-700 dark:text-champagne-400 border-b border-brand-200 dark:border-brand-900/40 pb-2">
              <span class="flex items-center space-x-1.5">
                <i data-lucide="info" class="w-3.5 h-3.5 text-brand-500"></i>
                <span>PRAGMA Column Schema Definition</span>
              </span>
              <span class="text-slate-400 font-normal">SQLite Definition</span>
            </div>
            <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-2 text-xs">
""")
        for col in columns_info:
            cname = col["name"]
            ctype = col["type"] or "TEXT"
            ispk = col["pk"]
            isnotnull = col["notnull"]
            pk_badge = '<span class="ml-1 text-[9px] px-1 py-0.2 rounded bg-amber-500/20 text-amber-600 dark:text-amber-400 font-bold border border-amber-500/30">PK</span>' if ispk else ''
            
            html_lines.append(f"""
              <div class="p-2 rounded-xl bg-white dark:bg-[#16060F] border border-brand-100 dark:border-brand-900/40">
                <div class="font-mono font-bold text-slate-800 dark:text-white flex items-center justify-between">
                  <span class="truncate">{cname}</span>
                  {pk_badge}
                </div>
                <div class="text-[10px] font-mono text-brand-600 dark:text-brand-300 mt-1 flex items-center justify-between">
                  <span>{ctype}</span>
                  <span class="text-slate-400">{"req" if isnotnull else "opt"}</span>
                </div>
              </div>""")

        html_lines.append(f"""
            </div>
          </div>

          <!-- Filter Count Pill -->
          <div id="filter-status-{tbl}" class="hidden text-xs text-slate-500 dark:text-champagne-400 font-medium"></div>

          <!-- Data Table Grid -->
          <div class="overflow-x-auto rounded-2xl border border-brand-200 dark:border-brand-900/60 max-h-[680px] overflow-y-auto">
            <table class="w-full text-left text-xs border-collapse" id="grid-{tbl}">
              <thead class="sticky top-0 z-10 bg-slate-100 dark:bg-[#200714] text-slate-600 dark:text-champagne-400 font-bold tracking-wider text-[11px] border-b border-brand-200 dark:border-brand-900/80 shadow-sm">
                <tr>
                  {"".join(f'<th class="py-3 px-3.5 whitespace-nowrap">{c.replace("_", " ").upper()}</th>' for c in col_names)}
                  <th class="py-3 px-3.5 text-right text-red-500 whitespace-nowrap">ACTIONS</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-brand-100 dark:divide-brand-900/40 font-medium bg-white dark:bg-[#16060F]">
""")

        if rows:
            for r in rows:
                rec_id = r["id"] if "id" in r.keys() else 0
                label_val = r["name"] if "name" in r.keys() else (r["email"] if "email" in r.keys() else (r["title"] if "title" in r.keys() else f"#{rec_id}"))
                label_escaped = str(label_val).replace("'", "\\'").replace('"', '&quot;')

                html_lines.append(f"""              <tr id="row-{tbl}-{rec_id}" class="hover:bg-brand-50/50 dark:hover:bg-brand-900/25 transition">""")
                for c in col_names:
                    val = r[c]
                    
                    if val is None:
                        cell_str = '<span class="text-slate-400 dark:text-slate-600 font-mono">-</span>'
                    elif c == "id":
                        cell_str = f'<span class="font-mono font-bold text-champagne-500">#{val}</span>'
                    elif isinstance(val, float) and any(kw in c for kw in ["cost", "price", "budget", "amount", "total", "tariff"]):
                        cell_str = f'<span class="font-bold text-brand-600 dark:text-champagne-400 font-mono">₹{val:,.2f}</span>'
                    elif isinstance(val, int) and any(kw in c for kw in ["cost", "price", "budget", "amount"]):
                        cell_str = f'<span class="font-bold text-brand-600 dark:text-champagne-400 font-mono">₹{val:,}</span>'
                    elif c in ["role"]:
                        role_str = str(val).lower()
                        if "operator" in role_str:
                            badge_bg = "bg-amber-500/15 text-amber-700 dark:text-amber-300 border border-amber-500/30"
                        elif "admin" in role_str:
                            badge_bg = "bg-purple-500/15 text-purple-700 dark:text-purple-300 border border-purple-500/30"
                        elif "business" in role_str:
                            badge_bg = "bg-blue-500/15 text-blue-700 dark:text-blue-300 border border-blue-500/30"
                        else:
                            badge_bg = "bg-brand-500/15 text-brand-700 dark:text-champagne-400 border border-brand-500/30"
                        cell_str = f'<span class="px-2 py-0.5 rounded-md text-[10px] font-extrabold uppercase {badge_bg}">{val}</span>'
                    elif c in ["status", "booking_status", "approval_status"]:
                        val_str = str(val).lower()
                        if any(k in val_str for k in ["active", "confirmed", "approved"]):
                            badge_bg = "bg-emerald-500/15 text-emerald-700 dark:text-emerald-300 border border-emerald-500/30"
                        elif any(k in val_str for k in ["pending", "in-review"]):
                            badge_bg = "bg-amber-500/15 text-amber-700 dark:text-amber-300 border border-amber-500/30"
                        elif any(k in val_str for k in ["disrupted", "cancelled", "rejected"]):
                            badge_bg = "bg-red-500/15 text-red-700 dark:text-red-300 border border-red-500/30"
                        else:
                            badge_bg = "bg-slate-500/15 text-slate-700 dark:text-slate-300 border border-slate-500/30"
                        cell_str = f'<span class="px-2 py-0.5 rounded-full text-[10px] font-bold {badge_bg}">{val}</span>'
                    elif isinstance(val, (int, bool)) and c in ["is_active", "verified", "available", "is_disrupted"]:
                        is_true = bool(val)
                        badge_bg = "bg-emerald-500/15 text-emerald-600 dark:text-emerald-400 border border-emerald-500/30" if is_true else "bg-slate-500/15 text-slate-500 dark:text-slate-400 border border-slate-500/30"
                        cell_str = f'<span class="px-2 py-0.5 rounded-md text-[10px] font-bold {badge_bg}">{"True" if is_true else "False"}</span>'
                    else:
                        str_val = str(val)
                        if len(str_val) > 70:
                            short_val = str_val[:65] + "..."
                            escaped_title = str_val.replace('"', '&quot;')
                            cell_str = f'<span class="text-slate-700 dark:text-slate-300 truncate max-w-[260px] inline-block" title="{escaped_title}">{short_val}</span>'
                        else:
                            cell_str = f'<span class="text-slate-700 dark:text-slate-300">{str_val}</span>'
                            
                    html_lines.append(f'                  <td class="py-3 px-3.5 whitespace-nowrap">{cell_str}</td>')
                
                # Action: Delete Button
                html_lines.append(f"""                  <td class="py-3 px-3.5 text-right whitespace-nowrap">
                    <button 
                      onclick="promptDeleteRecord('{tbl}', {rec_id}, '{label_escaped}')"
                      class="px-2.5 py-1 rounded-lg bg-red-500/10 hover:bg-red-600 text-red-600 dark:text-red-400 hover:text-white border border-red-500/20 font-bold transition text-[11px] inline-flex items-center space-x-1"
                      title="Delete record #{rec_id} from {tbl}">
                      <i data-lucide="trash-2" class="w-3.5 h-3.5"></i>
                      <span>Delete</span>
                    </button>
                  </td>""")
                html_lines.append("                </tr>")
        else:
            html_lines.append(f'                <tr><td colspan="{len(col_names) + 1}" class="py-12 text-center text-slate-400 dark:text-slate-500">No records found in table {tbl}</td></tr>')

        html_lines.append("""
              </tbody>
            </table>
          </div>
        </div>
""")

    html_lines.append("""
      </main>

      <!-- =====================================================================
           3. FULL MULTI-COLUMN LUXURY TRAVORA FOOTER
           ===================================================================== -->
      <footer class="pt-14 pb-10 border-t border-brand-200 dark:border-brand-900/60 space-y-12">
        
        <!-- Main Footer Columns -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-8 lg:gap-10">
          
          <!-- Column 1 & 2: Brand, Tagline & Trust Badges -->
          <div class="lg:col-span-2 space-y-4">
            <a href="/" class="inline-block">
              <img 
                src="/static/assets/logo/travora_logo_horizontal.png" 
                alt="TRAVORA" 
                class="h-10 w-auto object-contain"
              />
            </a>
            
            <p class="text-xs font-bold text-brand-600 dark:text-champagne-400">
              India's Leading AI-Powered Travel & Dynamic Tour Operations Platform
            </p>
            
            <p class="text-xs text-slate-500 dark:text-slate-400 leading-relaxed max-w-sm">
              Connecting millions of travelers with verified tour operators, luxury accommodations, and real-time autonomous itinerary recovery across 802 Indian districts.
            </p>
            
            <div class="pt-2 flex flex-wrap gap-2 text-xs">
              <span class="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-slate-100 dark:bg-[#1C050D] border border-brand-200 dark:border-brand-900/60 text-[10px] font-bold text-slate-700 dark:text-slate-300">
                <i data-lucide="shield-check" class="w-3.5 h-3.5 text-brand-600 dark:text-champagne-400"></i>
                <span>IATA Accredited Agency</span>
              </span>
              <span class="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-slate-100 dark:bg-[#1C050D] border border-brand-200 dark:border-brand-900/60 text-[10px] font-bold text-slate-700 dark:text-slate-300">
                <i data-lucide="train" class="w-3.5 h-3.5 text-blue-500"></i>
                <span>IRCTC Authorized Partner</span>
              </span>
              <span class="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-slate-100 dark:bg-[#1C050D] border border-brand-200 dark:border-brand-900/60 text-[10px] font-bold text-emerald-600 dark:text-emerald-400">
                <i data-lucide="database" class="w-3.5 h-3.5"></i>
                <span>SQLite 3.x WAL Mirror</span>
              </span>
            </div>
          </div>

          <!-- Column 3: Database Domain Tables -->
          <div class="space-y-3">
            <h4 class="text-xs font-black tracking-wider uppercase text-slate-900 dark:text-white">
              Data Domains
            </h4>
            <ul class="space-y-2 text-xs text-slate-600 dark:text-slate-400">
              <li><button onclick="filterCategory('Core Tourism')" class="hover:text-brand-600 dark:hover:text-champagne-400 transition">Core Tourism (6)</button></li>
              <li><button onclick="filterCategory('Itineraries')" class="hover:text-brand-600 dark:hover:text-champagne-400 transition">Dynamic Itineraries (4)</button></li>
              <li><button onclick="filterCategory('Commerce')" class="hover:text-brand-600 dark:hover:text-champagne-400 transition">Commercial & Bookings (5)</button></li>
              <li><button onclick="filterCategory('Intelligence')" class="hover:text-brand-600 dark:hover:text-champagne-400 transition">Disruption & AI Twin (4)</button></li>
              <li><button onclick="filterCategory('Users & Access')" class="hover:text-brand-600 dark:hover:text-champagne-400 transition">Users & Access Control (4)</button></li>
            </ul>
          </div>

          <!-- Column 4: Platform Applications -->
          <div class="space-y-3">
            <h4 class="text-xs font-black tracking-wider uppercase text-slate-900 dark:text-white">
              Platform Portals
            </h4>
            <ul class="space-y-2 text-xs text-slate-600 dark:text-slate-400">
              <li><a href="/" class="hover:text-brand-600 dark:hover:text-champagne-400 transition">Traveler Experience Portal</a></li>
              <li><a href="/?view=admin" class="hover:text-brand-600 dark:hover:text-champagne-400 transition">Central Telemetry Dashboard</a></li>
              <li><a href="/?view=weather_twin" class="hover:text-brand-600 dark:hover:text-champagne-400 transition">Weather Digital Twin</a></li>
              <li><a href="/?view=business_operator" class="hover:text-brand-600 dark:hover:text-champagne-400 transition">Corporate Travel Delegations</a></li>
              <li><a href="/docs" target="_blank" class="hover:text-brand-600 dark:hover:text-champagne-400 transition flex items-center space-x-1"><span>FastAPI Swagger Docs</span> <i data-lucide="external-link" class="w-3 h-3"></i></a></li>
            </ul>
          </div>

          <!-- Column 5: Security & Infrastructure -->
          <div class="space-y-3">
            <h4 class="text-xs font-black tracking-wider uppercase text-slate-900 dark:text-white">
              Security & Engine
            </h4>
            <div class="p-3.5 rounded-2xl bg-white dark:bg-[#16060F] border border-brand-200 dark:border-brand-900/60 space-y-2 text-[11px]">
              <div class="flex items-center justify-between">
                <span class="text-slate-500">Security Gate:</span>
                <span class="font-bold text-emerald-500">PIN Protected</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-slate-500">Engine:</span>
                <span class="font-mono text-slate-800 dark:text-slate-200">SQLite 3.x</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-slate-500">ACID Mode:</span>
                <span class="font-mono text-champagne-400">WAL Journal</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-slate-500">Auto-Sync:</span>
                <span class="font-bold text-emerald-500">Active Hook</span>
              </div>
            </div>
            
            <button 
              onclick="window.scrollTo({ top: 0, behavior: 'smooth' })" 
              class="w-full py-2 rounded-xl bg-slate-100 dark:bg-[#1C050D] hover:bg-brand-600 hover:text-white text-xs font-bold text-slate-700 dark:text-slate-300 border border-brand-200 dark:border-brand-900/60 transition flex items-center justify-center space-x-1.5">
              <i data-lucide="arrow-up" class="w-3.5 h-3.5"></i>
              <span>Back to Top</span>
            </button>
          </div>

        </div>

        <!-- Bottom Copyright Bar -->
        <div class="pt-8 border-t border-brand-200 dark:border-brand-900/50 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-slate-500 dark:text-slate-400">
          <div class="flex items-center space-x-2">
            <img 
              src="/static/assets/logo/travora_emblem.png" 
              alt="TRAVORA Emblem" 
              class="w-5 h-5 object-contain"
            />
            <span>&copy; 2026 TRAVORA Technologies Pvt. Ltd. All rights reserved.</span>
          </div>
          
          <div class="flex items-center space-x-4 text-[11px] font-mono">
            <span class="flex items-center space-x-1 text-emerald-500">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
              <span>All Systems Operational</span>
            </span>
            <span class="text-slate-400 dark:text-slate-600">•</span>
            <span>Version 3.4.2</span>
          </div>
        </div>

      </footer>

    </div>
  </div>

  <!-- JAVASCRIPT LOGIC -->
  <script>
    const API_BASE = window.location.origin.includes('http') ? window.location.origin : 'http://127.0.0.1:8000';
    const AUTH_KEY = 'travora_db_auth_token';

    // -------------------------------------------------------------------------
    // 1. Authentication & Security Gate (Password: 123)
    // -------------------------------------------------------------------------
    function checkAuthOnLoad() {
      const isAuthed = sessionStorage.getItem(AUTH_KEY) === 'granted';
      const gate = document.getElementById('auth-gate');
      const main = document.getElementById('main-studio-app');
      
      if (isAuthed) {
        if (gate) gate.classList.add('hidden');
        if (main) main.classList.remove('hidden');
      } else {
        if (gate) gate.classList.remove('hidden');
        if (main) main.classList.add('hidden');
        setTimeout(() => {
          const pinInput = document.getElementById('pin-input');
          if (pinInput) pinInput.focus();
        }, 120);
      }
    }

    function verifyPin() {
      const pinInput = document.getElementById('pin-input');
      const pin = (pinInput ? pinInput.value : '').trim();
      const errorBox = document.getElementById('auth-error-msg');
      const card = document.getElementById('auth-card');
      
      if (pin === '123') {
        if (errorBox) errorBox.classList.add('hidden');
        sessionStorage.setItem(AUTH_KEY, 'granted');
        
        // Success animation
        const btn = document.getElementById('unlock-btn');
        if (btn) {
          btn.innerHTML = '<i data-lucide="check" class="w-4 h-4 text-emerald-400"></i><span>Access Granted!</span>';
          btn.classList.remove('bg-brand-600', 'hover:bg-brand-700');
          btn.classList.add('bg-emerald-600');
        }
        if (window.lucide) lucide.createIcons();
        
        setTimeout(() => {
          const gate = document.getElementById('auth-gate');
          const main = document.getElementById('main-studio-app');
          if (gate) {
            gate.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
            gate.style.opacity = '0';
            gate.style.transform = 'scale(1.02)';
            setTimeout(() => gate.classList.add('hidden'), 400);
          }
          if (main) main.classList.remove('hidden');
          if (window.lucide) lucide.createIcons();
          showToast('Welcome to TRAVORA Database Studio', 'success');
        }, 300);
      } else {
        if (errorBox) {
          errorBox.classList.remove('hidden');
          errorBox.innerText = 'Access Denied: Incorrect Security Key. (Hint: 123)';
        }
        if (card) {
          card.classList.add('animate-shake');
          setTimeout(() => card.classList.remove('animate-shake'), 500);
        }
        if (pinInput) {
          pinInput.value = '';
          pinInput.focus();
        }
      }
    }

    function togglePinVisibility() {
      const pinInput = document.getElementById('pin-input');
      const eyeIcon = document.getElementById('eye-icon');
      if (!pinInput) return;
      const isPass = pinInput.type === 'password';
      pinInput.type = isPass ? 'text' : 'password';
      if (eyeIcon) {
        eyeIcon.setAttribute('data-lucide', isPass ? 'eye-off' : 'eye');
        if (window.lucide) lucide.createIcons();
      }
    }

    function lockStudio() {
      sessionStorage.removeItem(AUTH_KEY);
      const gate = document.getElementById('auth-gate');
      const main = document.getElementById('main-studio-app');
      if (gate) {
        gate.style.opacity = '1';
        gate.style.transform = 'none';
        gate.classList.remove('hidden');
      }
      if (main) main.classList.add('hidden');
      const pinInput = document.getElementById('pin-input');
      if (pinInput) {
        pinInput.value = '';
        pinInput.focus();
      }
      const btn = document.getElementById('unlock-btn');
      if (btn) {
        btn.innerHTML = '<i data-lucide="unlock" class="w-4 h-4"></i><span>Unlock Database Studio</span>';
        btn.classList.remove('bg-emerald-600');
        btn.classList.add('bg-brand-600', 'hover:bg-brand-700');
      }
      if (window.lucide) lucide.createIcons();
      showToast('Database Studio Locked', 'info');
    }

    // -------------------------------------------------------------------------
    // 2. Video Controls
    // -------------------------------------------------------------------------
    function toggleHeroVideo() {
      const vid = document.getElementById('hero-video');
      const icon = document.getElementById('video-toggle-icon');
      const text = document.getElementById('video-toggle-text');
      if (!vid) return;

      if (vid.paused) {
        vid.play();
        if (icon) icon.setAttribute('data-lucide', 'pause');
        if (text) text.innerText = 'Pause Video';
      } else {
        vid.pause();
        if (icon) icon.setAttribute('data-lucide', 'play');
        if (text) text.innerText = 'Play Video';
      }
      if (window.lucide) lucide.createIcons();
    }

    // -------------------------------------------------------------------------
    // 3. Theme Management (Synchronized with TRAVORA)
    // -------------------------------------------------------------------------
    function applyTheme(theme) {
      const isDark = theme === 'dark';
      if (isDark) {
        document.documentElement.classList.add('dark');
        document.documentElement.setAttribute('data-theme', 'dark');
      } else {
        document.documentElement.classList.remove('dark');
        document.documentElement.setAttribute('data-theme', 'light');
      }
      
      const themeText = document.getElementById('theme-text');
      const themeIcon = document.getElementById('theme-icon');
      if (themeText) themeText.innerText = isDark ? 'Dark' : 'Light';
      if (themeIcon) {
        themeIcon.setAttribute('data-lucide', isDark ? 'moon' : 'sun');
      }
      
      localStorage.setItem('travora_theme', theme);
      if (window.lucide) lucide.createIcons();
    }

    function toggleTheme() {
      const isDark = document.documentElement.classList.contains('dark');
      applyTheme(isDark ? 'light' : 'dark');
    }

    // Initialize Theme
    const savedTheme = localStorage.getItem('travora_theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    applyTheme(savedTheme);

    // -------------------------------------------------------------------------
    // 4. Tab & Category Navigation
    // -------------------------------------------------------------------------
    function showTable(tableName) {
      document.querySelectorAll('.table-container').forEach(el => el.classList.add('hidden'));
      document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('bg-brand-600', 'text-white', 'shadow-lg', 'shadow-brand-600/30', 'border-brand-500');
        btn.classList.add('bg-white', 'dark:bg-[#16060F]', 'text-slate-700', 'dark:text-slate-300', 'border-brand-200', 'dark:border-brand-900/60');
      });
      
      const sec = document.getElementById('table-sec-' + tableName);
      if (sec) sec.classList.remove('hidden');
      
      const btn = document.getElementById('btn-' + tableName);
      if (btn) {
        btn.classList.add('bg-brand-600', 'text-white', 'shadow-lg', 'shadow-brand-600/30', 'border-brand-500');
        btn.classList.remove('bg-white', 'dark:bg-[#16060F]', 'text-slate-700', 'dark:text-slate-300', 'border-brand-200', 'dark:border-brand-900/60');
      }
      
      if (window.lucide) lucide.createIcons();
    }

    function filterCategory(category) {
      document.querySelectorAll('.cat-filter-btn').forEach(b => {
        b.classList.remove('bg-brand-600', 'text-white', 'font-bold');
        b.classList.add('bg-white', 'dark:bg-[#16060F]', 'text-slate-600', 'dark:text-slate-300');
      });
      
      const catEscaped = category.replace(/ /g, '_');
      const activeBtn = document.getElementById('cat-btn-' + catEscaped);
      if (activeBtn) {
        activeBtn.classList.add('bg-brand-600', 'text-white', 'font-bold');
        activeBtn.classList.remove('bg-white', 'dark:bg-[#16060F]', 'text-slate-600', 'dark:text-slate-300');
      }

      let firstVisibleTable = null;
      document.querySelectorAll('.tab-btn').forEach(tab => {
        const tabCat = tab.getAttribute('data-category');
        if (category === 'All Tables' || tabCat === category) {
          tab.classList.remove('hidden');
          if (!firstVisibleTable) {
            firstVisibleTable = tab.id.replace('btn-', '');
          }
        } else {
          tab.classList.add('hidden');
        }
      });

      if (firstVisibleTable) {
        showTable(firstVisibleTable);
      }
    }

    // -------------------------------------------------------------------------
    // 5. Data Grid Search & Tools
    // -------------------------------------------------------------------------
    function filterTable(tableName, query) {
      const q = query.toLowerCase().trim();
      const rows = document.querySelectorAll('#grid-' + tableName + ' tbody tr');
      let visibleCount = 0;
      
      rows.forEach(row => {
        const matches = row.innerText.toLowerCase().includes(q);
        row.style.display = matches ? '' : 'none';
        if (matches) visibleCount++;
      });

      const statusBox = document.getElementById('filter-status-' + tableName);
      if (statusBox) {
        if (q.length > 0) {
          statusBox.classList.remove('hidden');
          statusBox.innerText = `Filtering "${query}": showing ${visibleCount} of ${rows.length} rows`;
        } else {
          statusBox.classList.add('hidden');
        }
      }
    }

    function toggleSchemaInspector(tableName) {
      const box = document.getElementById('schema-box-' + tableName);
      if (box) {
        box.classList.toggle('hidden');
        if (window.lucide) lucide.createIcons();
      }
    }

    function exportTableCSV(tableName) {
      const table = document.getElementById('grid-' + tableName);
      if (!table) return;

      const rows = Array.from(table.querySelectorAll('tr'));
      const csv = rows.map(row => {
        const cols = Array.from(row.querySelectorAll('th, td'));
        const dataCols = cols.slice(0, cols.length - 1);
        return dataCols.map(c => {
          let text = c.innerText.replace(/"/g, '""').trim();
          return `"${text}"`;
        }).join(',');
      }).join('\\n');

      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.setAttribute('href', url);
      link.setAttribute('download', `travora_${tableName}_${new Date().toISOString().slice(0, 10)}.csv`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      showToast(`Exported ${tableName} to CSV!`, 'success');
    }

    function copyTableJSON(tableName) {
      const table = document.getElementById('grid-' + tableName);
      if (!table) return;

      const headers = Array.from(table.querySelectorAll('thead th'))
        .slice(0, -1)
        .map(th => th.innerText.toLowerCase().replace(/\\s+/g, '_').trim());

      const dataRows = Array.from(table.querySelectorAll('tbody tr'));
      const records = dataRows.map(tr => {
        const cells = Array.from(tr.querySelectorAll('td')).slice(0, -1);
        const obj = {};
        cells.forEach((td, idx) => {
          obj[headers[idx] || `col_${idx}`] = td.innerText.trim();
        });
        return obj;
      });

      const jsonStr = JSON.stringify(records, null, 2);
      navigator.clipboard.writeText(jsonStr).then(() => {
        showToast(`Copied ${records.length} records as JSON to clipboard!`, 'success');
      }).catch(() => {
        showToast('Failed to copy to clipboard', 'error');
      });
    }

    // -------------------------------------------------------------------------
    // 6. Delete Record Confirmation Modal & API
    // -------------------------------------------------------------------------
    let pendingDelete = null;

    function promptDeleteRecord(tableName, recordId, recordName) {
      pendingDelete = { tableName, recordId, recordName };
      document.getElementById('modal-table-name').innerText = tableName;
      document.getElementById('modal-record-id').innerText = '#' + recordId;
      document.getElementById('modal-record-label').innerText = recordName;
      
      const modal = document.getElementById('delete-modal');
      modal.classList.remove('hidden');
      
      const confirmBtn = document.getElementById('modal-confirm-btn');
      confirmBtn.onclick = executePendingDelete;
      
      if (window.lucide) lucide.createIcons();
    }

    function closeDeleteModal() {
      const modal = document.getElementById('delete-modal');
      modal.classList.add('hidden');
      pendingDelete = null;
    }

    window.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closeDeleteModal();
    });

    async function executePendingDelete() {
      if (!pendingDelete) return;
      const { tableName, recordId, recordName } = pendingDelete;
      closeDeleteModal();

      const endpoint = tableName === 'users' ? `${API_BASE}/api/crud/users/${recordId}` : `${API_BASE}/api/crud/${tableName}/${recordId}`;

      try {
        showToast(`Deleting #${recordId} from ${tableName}...`, 'info');
        const res = await fetch(endpoint, { method: 'DELETE' });
        
        if (!res.ok) {
          const err = await res.json().catch(() => ({ detail: 'Failed to delete record' }));
          throw new Error(err.detail || 'Delete failed');
        }

        // Visually remove row
        const row = document.getElementById(`row-${tableName}-${recordId}`);
        if (row) {
          row.style.transition = 'all 0.35s ease';
          row.style.opacity = '0';
          row.style.transform = 'scale(0.95)';
          setTimeout(() => row.remove(), 350);
        }

        // Update counts
        const countBadge = document.getElementById(`badge-count-${tableName}`);
        const tabCount = document.getElementById(`count-${tableName}`);
        const kpiTotal = document.getElementById('kpi-total-records');

        if (countBadge) {
          const curr = parseInt(countBadge.innerText.replace(/,/g, '')) || 1;
          countBadge.innerText = Math.max(0, curr - 1).toLocaleString() + ' records';
        }
        if (tabCount) {
          const curr = parseInt(tabCount.innerText.replace(/,/g, '')) || 1;
          tabCount.innerText = Math.max(0, curr - 1).toLocaleString();
        }
        if (kpiTotal) {
          const curr = parseInt(kpiTotal.innerText.replace(/,/g, '')) || 1;
          kpiTotal.innerText = Math.max(0, curr - 1).toLocaleString();
        }

        showToast(`Record #${recordId} deleted permanently from ${tableName}!`, 'success');
      } catch (err) {
        console.error(err);
        showToast(`Error: ${err.message}`, 'error');
      }
    }

    function refreshDatabaseView() {
      const btn = document.getElementById('refresh-btn');
      if (btn) {
        btn.querySelector('i')?.classList.add('animate-spin');
      }
      showToast('Re-synchronizing database view...', 'info');
      setTimeout(() => {
        window.location.reload();
      }, 400);
    }

    // -------------------------------------------------------------------------
    // 7. Toast Notifications
    // -------------------------------------------------------------------------
    function showToast(message, type = 'info') {
      const box = document.getElementById('toast-box');
      if (!box) return;
      const el = document.createElement('div');
      
      const bgColor = type === 'error' ? 'bg-red-600 border-red-700 text-white' :
                      type === 'success' ? 'bg-emerald-600 border-emerald-700 text-white' :
                      'bg-brand-600 border-brand-700 text-white';

      el.className = `pointer-events-auto px-4 py-3 rounded-2xl shadow-2xl text-xs font-bold border flex items-center space-x-2.5 transition-all duration-300 transform translate-y-2 opacity-0 ${bgColor}`;
      
      const iconName = type === 'error' ? 'alert-triangle' : (type === 'success' ? 'check-circle-2' : 'info');
      el.innerHTML = `<i data-lucide="${iconName}" class="w-4 h-4"></i><span>${message}</span>`;
      box.appendChild(el);
      
      if (window.lucide) lucide.createIcons();

      requestAnimationFrame(() => {
        el.classList.remove('translate-y-2', 'opacity-0');
      });

      setTimeout(() => {
        el.classList.add('opacity-0', 'translate-y-2');
        setTimeout(() => el.remove(), 400);
      }, 4000);
    }

    // -------------------------------------------------------------------------
    // 8. Lifecycle & Initialization
    // -------------------------------------------------------------------------
    document.addEventListener('DOMContentLoaded', () => {
      checkAuthOnLoad();
      if (window.lucide) {
        lucide.createIcons();
      }
    });
  </script>
</body>
</html>
""")

    with open(HTML_OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("".join(html_lines))
    print(f"Created HTML SQL Table Studio: {HTML_OUTPUT_PATH}")

    conn.close()

if __name__ == "__main__":
    generate_database_views()
