import json

story = json.load(open('story.json', encoding='utf-8'))
pt = json.load(open('story_pt.json', encoding='utf-8'))

def key_norm(s):
    # normalize CRLF/CR to LF, then escape LF as literal \n for the XUAT file
    return s.replace('\r\n', '\n').replace('\r', '\n').replace('\n', r'\n')

pairs = []
# indexed story dialogues
for idx, val in pt.items():
    en = story[int(idx)]
    pairs.append((key_norm(en), key_norm(val)))

# testimony (exact string from assets)
testimony = ("Yes, I saw it. I couldn't believe my eyes... pineapple\r\n"
             "and pizza... together? I don't know his name, but he's\r\n"
             "been here a few times before, and I remember him since\r\n"
             "he always leaves the lowest percentage tip every time\r\n"
             "he pays, but this... this takes it to another level.")
testimony_pt = ("Sim, eu vi. Não pude acreditar nos meus olhos... abacaxi\r\n"
                "e pizza... juntos? Não sei o nome dele, mas ele já\r\n"
                "esteve aqui algumas vezes antes, e eu me lembro dele porque\r\n"
                "ele sempre deixa a menor porcentagem de gorjeta toda vez\r\n"
                "que paga, mas isto... isto vai a outro nível.")
pairs.append((key_norm(testimony), key_norm(testimony_pt)))

out = '\n'.join(f'{k}={v}' for k, v in pairs) + '\n'
open('DatabaseDetective_story_ptbr.txt', 'w', encoding='utf-8').write(out)
print(f"wrote {len(pairs)} story entries")
for k, v in pairs[:3]:
    print("  KEY:", k[:70]); print("  VAL:", v[:70]); print()
