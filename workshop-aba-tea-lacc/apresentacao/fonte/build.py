import json, re, sys, os
deck = sys.argv[1]; out_html = sys.argv[2]; notes_html = sys.argv[3] if len(sys.argv) > 3 else None
d = json.load(open(os.path.join(deck, 'project/deck.json')))
icons = {'Check': '✓', 'Warning': '!', 'Chat': '?', 'Book': '§', 'Lock': '×', 'Users': '●', 'Lightbulb': '★', 'Clock': '◷'}
secs = []; notes = []
for sid in d['order']:
    p = os.path.join(deck, 'project/slides', sid + '.html')
    if not os.path.exists(p): continue
    s = open(p, encoding='utf-8').read()
    m = re.search(r'<aside>(.*?)</aside>', s, re.S)
    notes.append((sid, m.group(1).strip() if m else ''))
    s = re.sub(r'<aside>.*?</aside>', '', s, flags=re.S)
    def ic(m):
        name = m.group(1); style = m.group(2)
        col = re.search(r'color:([^;"]+)', style); col = col.group(1) if col else '#2F5D8A'
        return f'<span class="ic" style="color:{col};border-color:{col}">{icons.get(name, "•")}</span>'
    s = re.sub(r'<x-icon name="(\w+)" style="([^"]*)"></x-icon>', ic, s)
    secs.append(s)
css = """
@page { size: 1920px 1080px; margin: 0 }
html, body { margin: 0; padding: 0; background: #2b2f36 }
* { box-sizing: border-box }
section { width: 1920px; height: 1080px; position: relative; overflow: hidden; page-break-after: always; break-after: page; margin: 0 auto }
h1, h2, h3, p, ul, ol, li { margin: 0 }
hr { margin: 0; border: none }
table { border-collapse: collapse }
.ic { display: inline-flex; align-items: center; justify-content: center; width: 56px; height: 56px; min-width: 56px; border: 4px solid; border-radius: 50%; font: 700 30px 'Public Sans', Arial, sans-serif }
@media screen { section { margin: 0 auto 24px auto; transform-origin: top left } }
"""
head = ('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
        f'<title>{d["title"]}</title>'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@400..700&family=Public+Sans:wght@400..700&display=swap">'
        f'<style>{css}</style></head><body>')
open(out_html, 'w', encoding='utf-8').write(head + '\n'.join(secs) + '</body></html>')
if notes_html:
    rows = ''.join(f'<h2>Slide {i+1} <small>({sid})</small></h2><p>{n}</p>' for i, (sid, n) in enumerate(notes))
    open(notes_html, 'w', encoding='utf-8').write('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Notas</title><style>@page{size:A4;margin:18mm} body{font:12pt "Public Sans",Arial,sans-serif;color:#1F2A37} h1{font-family:"Source Serif 4",Georgia,serif} h2{font-size:13pt;margin:14pt 0 4pt;color:#2F5D8A} small{color:#5B6675;font-weight:400} p{margin:0;line-height:1.45}</style><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@400..700&family=Public+Sans:wght@400..700&display=swap"></head><body><h1>Workshop ABA e TEA — notas da palestrante</h1>' + rows + '</body></html>')
print(len(secs), 'slides')
