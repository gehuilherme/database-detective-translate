import urllib.request, urllib.parse, json, time, re, sys, os

sents = json.load(open('remaining_sentences.json', encoding='utf-8'))

# extra noise filter (internal/debug/sql that slipped through)
def is_noise(s):
    st = s.strip()
    if re.search(r'->|={|error=|\bParse[A-Z]|\bGet[A-Z]\w+\(|VALUES|\.log\b|\.text\.Length|Assembly-CSharp|, Scripts\b|#Level|firstName|lastName|selectColumn|messageCode|messageType|waitDuration|caseHints|queryHints|currentTime|_[A-Z][a-z]', st):
        return True
    # pure format/placeholder strings
    if len(re.sub(r'\{\d+\}|[^A-Za-z]', '', st)) < 6:
        return True
    # SQL DDL-ish
    if re.search(r'\b(TEXT|INT|REAL|BLOB)\b.*\b(TEXT|INT|REAL|PRIMARY|FOREIGN)\b', st):
        return True
    return False

work = [s for s in sents if not is_noise(s)]
print(f"MT queue: {len(work)} / {len(sents)}", flush=True)

def protect(s):
    tokens = []
    def repl(m):
        tokens.append(m.group(0)); return f"⟦{len(tokens)-1}⟧"
    # protect TMP/rich-text tags and {0} placeholders
    p = re.sub(r'<[^>]+>|\{\d+\}', repl, s)
    # translate on a single line (google mangles newlines); remember nothing—key stays exact
    p = p.replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')
    return p, tokens

def restore(t, tokens):
    for i, tok in enumerate(tokens):
        t = t.replace(f"⟦{i}⟧", tok).replace(f"⟦ {i} ⟧", tok)
    return t

def gt(text, tl='pt', tries=4):
    url = 'https://translate.googleapis.com/translate_a/single?' + urllib.parse.urlencode(
        {'client': 'gtx', 'sl': 'en', 'tl': tl, 'dt': 't', 'q': text})
    for a in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=25) as r:
                data = json.load(r)
            return ''.join(seg[0] for seg in data[0] if seg[0])
        except Exception as e:
            time.sleep(1.5 * (a + 1))
    return None

out = {}
if os.path.exists('mt_results.json'):
    out = json.load(open('mt_results.json', encoding='utf-8'))
count = 0
for s in work:
    if s in out:
        continue
    p, toks = protect(s)
    tr = gt(p)
    if tr is None:
        continue
    out[s] = restore(tr, toks)
    count += 1
    if count % 25 == 0:
        json.dump(out, open('mt_results.json', 'w', encoding='utf-8'), ensure_ascii=False)
        print(f"  {count} translated...", flush=True)
    time.sleep(0.25)
json.dump(out, open('mt_results.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(f"DONE. total translated: {len(out)}", flush=True)
