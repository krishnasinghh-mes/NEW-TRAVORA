import os, re

# Look for patterns that cause literal '}' or '{' to be rendered
pats = [
    re.compile(r'\}\`\s*:\s*\'\''),
    re.compile(r'\}\`\s*:\s*\`'),
    re.compile(r'\</option\>\}\`'),
    re.compile(r'\<div[^\>]*\>\s*\}\s*\</div\>'),
    re.compile(r'\}\s*\}\`'),
    re.compile(r'^\s*\}\s*$')
]

with open('strays_found.txt', 'w', encoding='utf-8') as out:
    for root, dirs, files in os.walk('static/js'):
        for f in files:
            if f.endswith('.js') and not '.bak' in f:
                p = os.path.join(root, f)
                with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                    for idx, line in enumerate(fp):
                        for pat in pats:
                            if pat.search(line):
                                out.write(f"{p}:{idx+1} -> {line.strip()}\n")

print("Saved strays_found.txt")
