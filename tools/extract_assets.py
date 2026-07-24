import UnityPy, os, re, json, struct

GAME = r"c:/Program Files (x86)/Steam/steamapps/common/Database Detective/copOS_Data"
files = ["resources.assets", "sharedassets0.assets", "sharedassets1.assets",
         "sharedassets2.assets", "level0", "level1", "level2",
         "globalgamemanagers.assets"]

def extract_unity_strings(data):
    """Scan raw serialized bytes for Unity strings: int32-LE length + UTF-8, 4-aligned."""
    out = []
    n = len(data); i = 0
    while i + 4 <= n:
        ln = struct.unpack_from('<i', data, i)[0]
        if 3 <= ln <= 6000 and i + 4 + ln <= n:
            chunk = data[i+4:i+4+ln]
            # skip if the chunk itself begins with an int32 length prefix (nested) -> let inner match handle it
            if ln >= 8:
                inner = struct.unpack_from('<i', chunk, 0)[0]
                if inner == ln - 4 or inner == ln - 8:
                    i += 4; continue
            try:
                s = chunk.decode('utf-8')
            except Exception:
                i += 4; continue
            printable = sum(1 for c in s if c.isprintable() or c in '\n\r\t')
            if printable >= len(s) * 0.97 and re.search(r'[A-Za-z]', s) and ' ' in s and '�' not in s:
                out.append(s)
                pad = (4 - (ln % 4)) % 4
                i += 4 + ln + pad
                continue
        i += 4
    return out

all_strings = {}
for fn in files:
    path = os.path.join(GAME, fn)
    if not os.path.exists(path):
        continue
    try:
        env = UnityPy.load(path)
    except Exception as e:
        print("load fail", fn, e); continue
    cnt = 0
    for obj in env.objects:
        if obj.type.name in ("MonoBehaviour", "TextAsset"):
            try:
                data = obj.get_raw_data()
            except Exception:
                continue
            for s in extract_unity_strings(data):
                all_strings.setdefault(s, [0, set()])
                all_strings[s][0] += 1
                all_strings[s][1].add(fn)
                cnt += 1
    print(f"{fn}: {cnt} string occurrences, {len(env.objects)} objects")

# save
res = {s: {"count": v[0], "files": sorted(v[1])} for s, v in all_strings.items()}
json.dump(res, open('asset_strings.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print("\nTOTAL distinct asset strings:", len(res))
# probe
for probe in ["pineapple", "saw it", "Testimony", "Clue", "believe my eyes", "percentage tip"]:
    hits = [s for s in res if probe.lower() in s.lower()]
    print(f"[{probe}] {len(hits)}", "| "+repr(hits[0][:80]) if hits else "")
