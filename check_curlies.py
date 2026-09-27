import os, sqlite3

print("Searching DB...")
if os.path.exists('travora.db'):
    conn = sqlite3.connect('travora.db')
    cur = conn.cursor()
    tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
    for t in tables:
        cols = [c[1] for c in cur.execute(f"PRAGMA table_info({t})").fetchall()]
        for c in cols:
            try:
                matches = cur.execute(f"SELECT id, {c} FROM {t} WHERE CAST({c} AS TEXT) LIKE '%{{%'").fetchall()
                if matches:
                    print(f"Match in {t}.{c}: {len(matches)} rows")
                    for m in matches[:3]:
                        print("  sample:", str(m)[:100])
            except Exception as e:
                pass

print("\nSearching files for '{{' or '{{{' ...")
for root, dirs, files in os.walk('.'):
    if '.venv' in root or '__pycache__' in root or '.git' in root:
        continue
    for f in files:
        if f.endswith(('.js', '.html', '.py', '.css', '.json', '.md')):
            p = os.path.join(root, f)
            try:
                with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                    for i, line in enumerate(fp):
                        if '{{' in line or '{ { {' in line:
                            print(f"{p}:{i+1} -> {line.strip()[:100]}")
            except Exception as e:
                pass
