import re, json, urllib.request, urllib.parse, time
p = r"c:/Program Files (x86)/Steam/steamapps/common/Database Detective/copOS_Data/resources.assets"
data = open(p, 'rb').read()
idx = data.find(b'Tip percentages')
seg = data[idx-45000:idx+45000].decode('utf-8', 'replace')
lines = re.findall(r'(\d+;\d+;\d+;[^\r\n\x00]{5,600})', seg)
hints = []; seen = set()
for ln in lines:
    txt = ln.split(';', 3)[3]
    rendered = re.sub(r'\\+n', '\n', txt).replace('\\"', '"').strip()
    if rendered not in seen and len(rendered) > 8 and re.search(r'[a-z]', rendered):
        seen.add(rendered); hints.append(rendered)
print("hints:", len(hints), flush=True)

def protect(s):
    toks = []
    def r(m): toks.append(m.group(0)); return f"⟦{len(toks)-1}⟧"
    return re.sub(r'<[^>]+>|\{\d+\}', r, s).replace('\n', ' '), toks
def restore(t, toks):
    for i, tk in enumerate(toks): t = t.replace(f"⟦{i}⟧", tk).replace(f"⟦ {i} ⟧", tk)
    return t
def gt(text, tries=4):
    url = 'https://translate.googleapis.com/translate_a/single?' + urllib.parse.urlencode({'client':'gtx','sl':'en','tl':'pt','dt':'t','q':text})
    for a in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=25) as r: d = json.load(r)
            return ''.join(x[0] for x in d[0] if x[0])
        except: time.sleep(1.2*(a+1))
    return None

res = {}
for h in hints:
    pr, toks = protect(h); tr = gt(pr)
    if tr: res[h] = restore(tr, toks)
    time.sleep(0.15)
json.dump(res, open('hints_results.json', 'w', encoding='utf-8'), ensure_ascii=False)
def esc(s): return s.replace('\r', r'\r').replace('\n', r'\n')
open('DatabaseDetective_hints_ptbr.txt', 'w', encoding='utf-8').write(
    '\n'.join(f'{esc(k)}={esc(v)}' for k, v in res.items()) + '\n')
print("DONE hints:", len(res), flush=True)
