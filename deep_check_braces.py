import os, re

patterns = [
    (re.compile(r'>\s*\}'), 'Stray >}'),
    (re.compile(r'\}\s*</'), 'Stray }</'),
    (re.compile(r'\}\s*`\s*:'), 'Stray }`:'),
    (re.compile(r'\}\s*`\s*\)'), 'Stray }`)'),
    (re.compile(r'\}\s*`\s*\}'), 'Stray }`}'),
    (re.compile(r'option>\}\`'), 'Stray option>}`'),
    (re.compile(r'\{{'), 'Stray {{'),
    (re.compile(r'\}\}'), 'Stray }}'),
    (re.compile(r'\{\s*\{\s*\{'), 'Stray { { {')
]

for root, dirs, files in os.walk('static/js'):
    for f in files:
        if f.endswith('.js') and not '.bak' in f:
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                for idx, line in enumerate(fp):
                    for pat, desc in patterns:
                        if pat.search(line):
                            print(f"[{desc}] {p}:{idx+1} -> {line.strip()}")
