import os, re

# Look for }` that is not part of a template string variable like ${var}`
pattern = re.compile(r'[^$]\{[^\}]*\}\`|^\s*\}\`|[^$]\}\`')

with open('curly_backtick_results.txt', 'w', encoding='utf-8') as out:
    for root, dirs, files in os.walk('static/js'):
        for f in files:
            if f.endswith('.js') and not '.bak' in f:
                p = os.path.join(root, f)
                with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                    for idx, line in enumerate(fp):
                        # check if line contains }` that might be an erroneous closing brace
                        if '}`' in line:
                            # if it's ${something}` it's valid, but if it ends with }` : or }` after html, it's suspect
                            out.write(f"{p}:{idx+1} -> {line.strip()}\n")

print("Saved curly_backtick_results.txt")
