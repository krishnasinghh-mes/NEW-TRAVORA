import os, difflib

for root, dirs, files in os.walk('static'):
    for f in files:
        if f.endswith('.bak'):
            orig_name = f[:-4]
            orig_path = os.path.join(root, orig_name)
            bak_path = os.path.join(root, f)
            if os.path.exists(orig_path):
                print(f"=== DIFF for {orig_name} ===")
                with open(bak_path, 'r', encoding='utf-8', errors='ignore') as f1:
                    lines1 = f1.readlines()
                with open(orig_path, 'r', encoding='utf-8', errors='ignore') as f2:
                    lines2 = f2.readlines()
                diff = list(difflib.unified_diff(lines1, lines2, fromfile='bak', tofile='curr', n=2))
                for line in diff[:40]:
                    print(line, end='')
                if len(diff) > 40:
                    print(f"... ({len(diff) - 40} more lines of diff)")
