// Lê o HTML gerado por build.py no Chromium e exporta, para cada slide, a posição e o estilo
// de cada bloco de texto, tabela, imagem e forma. O resultado alimenta gerar_pptx.py.
// Uso: node pptx_extrair.js slides.html layout.json
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const [src, out] = process.argv.slice(2);
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.goto('file://' + path.resolve(src));
  await page.evaluate(() => document.fonts.ready);
  await page.addStyleTag({ content: 'section{margin:0 0 0 0 !important}' });
  const data = await page.evaluate(() => {
    const px = v => parseFloat(v) || 0;
    const visibleBg = c => c && c !== 'rgba(0, 0, 0, 0)' && c !== 'transparent';
    function runs(el) {
      const out = [];
      (function walk(n) {
        for (const c of n.childNodes) {
          if (c.nodeType === 3) {
            const t = c.textContent.replace(/\s+/g, ' ');
            if (!t) continue;
            const cs = getComputedStyle(c.parentElement);
            out.push({ t, b: px(cs.fontWeight) >= 600, i: cs.fontStyle === 'italic', color: cs.color, size: px(cs.fontSize) });
          } else if (c.nodeType === 1) {
            if (c.tagName === 'BR') out.push({ t: '\n' });
            else walk(c);
          }
        }
      })(el);
      if (out.length) { out[0].t = out[0].t.replace(/^ /, ''); out[out.length - 1].t = out[out.length - 1].t.replace(/ $/, ''); }
      return out;
    }
    function textBlock(el, base) {
      const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
      return { x: r.left - base.left, y: r.top - base.top, w: r.width, h: r.height,
        size: px(cs.fontSize), lh: cs.lineHeight === 'normal' ? 1.2 : px(cs.lineHeight) / px(cs.fontSize),
        align: cs.textAlign, color: cs.color };
    }
    const slides = [];
    for (const sec of document.querySelectorAll('section')) {
      const base = sec.getBoundingClientRect();
      const items = [];
      const scs = getComputedStyle(sec);
      for (const el of sec.querySelectorAll('*')) {
        if (el.closest('aside') || el.tagName === 'ASIDE') continue;
        const r = el.getBoundingClientRect();
        if (!r.width || !r.height) continue;
        const cs = getComputedStyle(el);
        const tag = el.tagName;
        if (tag === 'IMG') {
          items.push({ kind: 'img', src: el.getAttribute('src'), x: r.left - base.left, y: r.top - base.top, w: r.width, h: r.height, alt: el.alt });
        } else if (tag === 'TABLE') {
          const rows = [...el.rows].map(tr => ({ bg: getComputedStyle(tr).backgroundColor,
            cells: [...tr.cells].map(td => { const b = textBlock(td, base); const cc = getComputedStyle(td);
              return { runs: runs(td), w: b.w, h: b.h, size: b.size, color: b.color, header: td.tagName === 'TH', bg: cc.backgroundColor, pad: px(cc.paddingLeft) }; }) }));
          items.push({ kind: 'table', x: r.left - base.left, y: r.top - base.top, w: r.width, h: r.height, rows });
        } else if (tag === 'UL' || tag === 'OL') {
          const b = textBlock(el, base);
          b.kind = 'list'; b.ordered = tag === 'OL';
          b.items = [...el.children].map(li => runs(li));
          b.gap = el.children.length > 1 ? px(getComputedStyle(el.children[1]).marginTop) : 0;
          items.push(b);
        } else if (['H1', 'H2', 'H3', 'P'].includes(tag) && !el.closest('table') && !el.closest('li')) {
          const b = textBlock(el, base); b.kind = 'text'; b.runs = runs(el);
          if (b.runs.length) items.push(b);
        } else if (tag === 'DIV' && visibleBg(cs.backgroundColor) && !el.textContent.trim()) {
          items.push({ kind: 'rect', x: r.left - base.left, y: r.top - base.top, w: r.width, h: r.height, bg: cs.backgroundColor });
        } else if (tag === 'DIV' && visibleBg(cs.backgroundColor)) {
          items.push({ kind: 'rect', x: r.left - base.left, y: r.top - base.top, w: r.width, h: r.height, bg: cs.backgroundColor, radius: px(cs.borderTopLeftRadius) });
        }
      }
      const aside = sec.querySelector('aside');
      slides.push({ id: sec.id, bg: scs.backgroundColor, items, notes: aside ? aside.textContent.trim() : '' });
    }
    return slides;
  });
  fs.writeFileSync(out, JSON.stringify(data, null, 1));
  console.log(data.length, 'slides');
  await browser.close();
})();
