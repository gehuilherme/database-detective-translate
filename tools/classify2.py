import json, re
d = json.load(open('us_scripts.json', encoding='utf-8'))
BS = chr(92)

def is_path(s): return '/' in s or BS in s

# ---- strong SKIP filter (internal / debug / sql / assets) ----
SQL_VERBS = ('SELECT ','SELECT\r','SELECT\n','INSERT ','UPDATE ','DELETE ','CREATE ','DROP ','ALTER ','WITH ','PRAGMA','BEGIN','COMMIT','ROLLBACK','REPLACE ')
DEBUG_WORDS = ('located at','Failed to','Finished loading','loaded.','loaded!','timestamped','culprit','rich presence','Rich presence','sqlite_master','photo clue','collection!','savedVolume','iconsMoved','iconPositions','stackTrace','Packsize','DllCheck','SteamAPI','Steamworks','Player.log','Player-prev','.log','Logfile','log files','logs','Minutes played','HasValue','overriding',' -> ','-> ','={','error=','BEFORE','AFTER','hasLoad','hasEveryone','Does not contain','Rolling back','Adding ','rows to','Creating tables','Level {0}','level {0}','level: {0}','Loading ','Setting ','Saving ','Saved Suit','Clearing','Incrementing','Data reset','Instantiat')

def is_debug(s):
    return any(w in s for w in DEBUG_WORDS)

def is_sql_ddl_or_query(s):
    if s.lstrip().startswith(SQL_VERBS): return True
    if re.search(r'\b(TEXT|INT|REAL|BLOB)\b.*\b(TEXT|INT|REAL|BLOB|PRIMARY KEY|FOREIGN KEY)\b', s): return True
    if 'PRIMARY KEY' in s or 'FOREIGN KEY' in s or 'REFERENCES' in s: return True
    if re.match(r'^[a-z_]+(,\s*[a-z_]+)+$', s): return True           # column csv
    if re.match(r'^[a-z_]+ (TEXT|INT|REAL|BLOB)\b', s): return True     # schema col
    if re.match(r'^[\'"]?\{\d+\}[\'"]?(,\s*[\'"]?\{\d+\}[\'"]?)+$', s): return True  # value tuples
    return False

def is_format_noise(s):
    t = re.sub(r'\{\d+\}', '', s)
    t = re.sub(r'[^A-Za-z]', '', t)
    return len(t) < 3

def skip(s):
    st = s.strip()
    if not st or is_path(st) or is_format_noise(st): return True
    if is_debug(st) or is_sql_ddl_or_query(st): return True
    # pure input-action / short identifier tokens handled later
    return False

survivors = [s for s in d if not skip(s)]

# ---- categorize survivors ----
def cat(s):
    st = s.strip()
    # SQL parser error: explanatory sentence about SQL
    if re.search(r'\b(statement|clause|keyword|aggregate|column|expression|parenthes|alias|operator|query|queries|comma|semicolon|token|identifier|condition|GROUP BY|ORDER BY|JOIN|SELECT|FROM|WHERE|USING|HAVING|AS)\b', st) \
       and re.search(r'\b(cannot|must|should|can only|need|needs|invalid|not allowed|missing|expected|unexpected|too many|at least|directly|conflicting|empty|already exists|no |not be|be given|be placed|start with|end with|contain|provide|specify|found)\b', st, re.I):
        return 'sql_error'
    # multiline dialogue (assistant/tutorial)
    if '\n' in st or BS+'n' in s:
        return 'dialogue'
    # website prose w/ TMP tags
    if any(t in st for t in ('<color','<link','<b>','</','<i>','<size','<u>')):
        return 'narrative'
    words = st.split()
    if st.endswith('?') or st.endswith('!'):
        return 'ui_notify'
    if len(words) >= 5:
        return 'narrative'
    if 1 <= len(words) <= 4:
        return 'ui_label'
    return 'review'

buckets = {}
for s in survivors:
    buckets.setdefault(cat(s), []).append(s)

order = ['sql_error','dialogue','ui_notify','narrative','ui_label','review']
print("survivors:", len(survivors))
for k in order:
    print(f"  {k}: {len(buckets.get(k,[]))}")
json.dump(buckets, open('buckets2.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
# write readable dumps per bucket
for k in order:
    with open(f'bucket_{k}.txt','w',encoding='utf-8') as f:
        for s in buckets.get(k,[]):
            f.write(repr(s)+"\n")
print("wrote bucket_*.txt")
