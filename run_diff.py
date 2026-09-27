import os, difflib

with open('diff_summary.txt', 'w', encoding='utf-8') as out:
    for root, dirs, files in os.walk('static'):
        for f in files:
            if f.endswith('.bak'):
                orig_name = f[:-4]
                orig_path = os.path.join(root, orig_name)
                bak_path = os.path.join(root, f)
                if os.path.exists(orig_path):
                    out.write(f"\n\n=== DIFF for {orig_name} ===\n")
                    with open(bak_path, 'r', encoding='utf-8', errors='ignore') as f1:
                        lines1 = f1.readlines()
                    with open(orig_path, 'r', encoding='utf-8', errors='ignore') as f2:
                        lines2 = f2.readlines()
                    diff = list(difflib.unified_diff(lines1, lines2, fromfile='bak', tofile='curr', n=2))
                    out.writelines(diff[:200])
                    if len(diff) > 200:
                        out.write(f"\n... ({len(diff) - 200} more lines)\n")

print("Saved diff_summary.txt")
