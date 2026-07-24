import json, re

ordered = json.load(open('targets_ordered.json', encoding='utf-8'))
pt = json.load(open('pt.json', encoding='utf-8'))
by_id = {o['id']: o['en'] for o in ordered}

# sanity: every pt id exists in targets
missing = [k for k in pt if k not in by_id]
if missing:
    raise SystemExit("pt.json ids not in targets: " + str(missing))

def esc(s):
    # escape for one-line XUAT entry
    return s.replace('\r', r'\r').replace('\n', r'\n')

def regex_escape_literal(s):
    return re.sub(r'([.^$*+?()\[\]{}|\\])', r'\\\1', s)

lines = []
regex_lines = []
covered = 0
for o in ordered:
    idd = o['id']; en = o['en']
    if idd not in pt:
        continue
    val = pt[idd]
    covered += 1
    if '=' in en:
        # XUAT splits key on first '=', so emit as a regex entry
        pat = '^' + regex_escape_literal(esc(en)) + '$'
        regex_lines.append(f'r:"{pat}"={esc(val)}')
    else:
        lines.append(f'{esc(en)}={esc(val)}')

# merge runtime-harvested UI extras (english=portuguese), excluding table/column names
import os
extra_count = 0
if os.path.exists('ui_extra.json'):
    extra = json.load(open('ui_extra.json', encoding='utf-8'))
    for en, val in extra.items():
        if en.startswith('_'):
            continue
        if '=' in en:
            pat = '^' + regex_escape_literal(esc(en)) + '$'
            regex_lines.append(f'r:"{pat}"={esc(val)}')
        else:
            lines.append(f'{esc(en)}={esc(val)}')
        extra_count += 1
print(f"ui_extra entries: {extra_count}")

out = '\n'.join(lines + regex_lines) + '\n'
open('DatabaseDetective_ptbr.txt', 'w', encoding='utf-8').write(out)
print(f"covered {covered}/{len(ordered)} target strings")
print(f"plain entries: {len(lines)}, regex entries: {len(regex_lines)}")
print("\n--- first 6 lines ---")
for l in lines[:6]:
    print(l)
print("--- regex entry ---")
for l in regex_lines:
    print(l)
