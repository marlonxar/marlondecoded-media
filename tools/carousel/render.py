#!/usr/bin/env python3
"""MarlonDecoded Instagram carousel renderer.
Usage: python3 render.py spec.json OUTDIR
Writes OUTDIR/<slug>-01.png ... (1080x1350). Requires: pip install playwright (Chromium)."""
import json, sys, os, re, html, glob
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
PAL = {
 "cobalt": ("#1736C9", "#FFE600", "#141447", "#141447"),
 "tomato": ("#E8432E", "#FFE600", "#2A0F0A", "#2A0F0A"),
 "forest": ("#0F6B45", "#FFD23F", "#082A1C", "#082A1C"),
 "plum": ("#4B1D78", "#5CFFB0", "#1A0830", "#1A0830"),
 "tangerine": ("#FF7A1A", "#1B1B3A", "#2B1405", "#FFFFFF"),
 "teal": ("#0E8C8C", "#FFDE59", "#052E2E", "#052E2E"),
 "graphite": ("#1E2230", "#FF4FA3", "#0A0C12", "#0A0C12"),
 "magenta": ("#C2187A", "#FFE600", "#2E0620", "#2E0620"),
}
KW = r"\b(public|private|protected|static|final|class|interface|enum|record|void|int|double|long|char|boolean|float|byte|short|new|return|if|else|for|while|do|switch|case|break|continue|try|catch|finally|throw|throws|extends|implements|this|super|null|true|false|var|import|package)\b"
TOK = re.compile(r'(?P<cm>//.*$)|(?P<st>"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')|(?P<kw>'+KW+r')|(?P<nu>\b\d+(?:\.\d+)?\b)', re.M)
def code_html(src):
    out, pos = [], 0
    for m in TOK.finditer(src):
        out.append(html.escape(src[pos:m.start()]))
        out.append(f'<span class="{m.lastgroup}">{html.escape(m.group())}</span>')
        pos = m.end()
    out.append(html.escape(src[pos:]))
    return "".join(out)
def md(t):
    t = html.escape(t)
    t = re.sub(r"`([^`]+)`", r'<code>\1</code>', t)
    t = re.sub(r"\*\*([^*]+)\*\*", r'<b>\1</b>', t)
    return t.replace("\n", "<br>")
def duotone(dark, light, out):
    from PIL import Image, ImageOps
    im = Image.open(os.path.join(HERE, "md_avatar.webp")).convert("L")
    im = ImageOps.autocontrast(im, cutoff=2)
    ImageOps.colorize(im, black=dark, white=light).save(out)
def build(spec):
    bg, sig, line, sigtext = PAL[spec.get("palette", "cobalt")]
    slides = spec["slides"]; n = len(slides) + 2
    css = f"""
@font-face{{font-family:BS;src:url('fonts/big-shoulders-display-latin-900-normal.woff2');font-weight:900}}
@font-face{{font-family:BS;src:url('fonts/big-shoulders-display-latin-800-normal.woff2');font-weight:800}}
@font-face{{font-family:MM;src:url('fonts/martian-mono-latin-wdth-normal.woff2');font-weight:100 800;font-stretch:75% 112.5%}}
@font-face{{font-family:CV;src:url('fonts/caveat-latin-700-normal.woff2');font-weight:700}}
*{{margin:0;padding:0;box-sizing:border-box}} body{{background:#000}}
.s{{position:relative;width:1080px;height:1350px;overflow:hidden;background:{bg};color:#fff;font-family:BS,'Noto Color Emoji',sans-serif}}
.s:before{{content:'';position:absolute;inset:0;background:
 repeating-linear-gradient(0deg,rgba(255,255,255,.07) 0 2px,transparent 2px 54px),
 repeating-linear-gradient(90deg,rgba(255,255,255,.07) 0 2px,transparent 2px 54px)}}
.s:after{{content:'';position:absolute;inset:0;background:radial-gradient(120% 90% at 50% 35%,transparent 55%,{line}aa 100%)}}
.in{{position:absolute;inset:0;z-index:2;padding:96px 84px}}
.top{{display:flex;align-items:center;gap:22px}}
.tav,.bav{{border-radius:50%;background:url('_av.png') center/cover;border:5px solid {sig};box-shadow:0 0 0 6px {line}}} .tav{{width:84px;height:84px}}
.mark{{font-weight:900;font-size:40px}} .ser{{margin-left:auto;font-weight:800;font-size:30px;opacity:.8}}
.rail{{position:absolute;left:0;top:0;height:14px;background:{sig};z-index:3}}
.cnt{{position:absolute;right:84px;bottom:72px;z-index:3;font-family:MM;font-stretch:75%;font-size:26px;opacity:.75}}
.swipe{{position:absolute;left:84px;bottom:66px;z-index:3;font-weight:900;font-size:44px;background:{sig};color:{sigtext};padding:10px 26px;border-radius:999px;box-shadow:6px 8px 0 {line}}}
.big{{font-weight:900;text-transform:uppercase;line-height:.9;letter-spacing:-1px}}
.ct .big{{font-size:150px;margin-top:150px}} .ct .hook{{font-family:CV;font-weight:700;font-size:64px;color:{sig};margin-top:44px;line-height:1.05;transform:rotate(-2deg)}}
.deco{{position:absolute;right:-40px;bottom:120px;z-index:1;font-family:MM;font-stretch:75%;font-weight:800;font-size:460px;color:rgba(255,255,255,.08);transform:rotate(-8deg)}} .stack{{position:absolute;left:84px;bottom:190px;z-index:2;font-family:MM;font-stretch:75%;font-size:30px;line-height:1.7;color:#fff;opacity:.9}} .stack i{{font-style:normal;color:{sig}}}
.hl{{background:linear-gradient(transparent 62%,{sig} 62% 92%,transparent 92%);color:#fff;padding:0 6px}}
.num{{font-family:MM;font-stretch:75%;font-weight:700;font-size:30px;color:{sig};margin-top:70px}}
h2{{font-weight:900;text-transform:uppercase;font-size:96px;line-height:.92;margin-top:16px}}
.body{{font-weight:800;font-size:46px;line-height:1.18;margin-top:34px;max-width:900px}}
.body code{{font-family:MM;font-stretch:75%;font-size:38px;background:{line};padding:2px 12px;border-radius:10px;color:{sig}}}
.body b{{color:{sig}}}
pre{{margin-top:40px;background:{line};border-radius:26px;padding:36px 40px;font-family:MM;font-stretch:75%;font-size:34px;line-height:1.45;color:#fff;box-shadow:10px 12px 0 rgba(0,0,0,.25);white-space:pre}}
pre .kw{{font-weight:800;color:{sig if sigtext!='#FFFFFF' else '#FFD9A8'}}} pre .st,pre .nu{{color:#FFB8D6}} pre .cm{{color:#9AA3C7}}
.note{{font-family:CV;font-weight:700;font-size:54px;color:{sig if sigtext!='#FFFFFF' else '#fff'};margin-top:34px;transform:rotate(-2deg)}}
.end{{text-align:center}} .bav{{width:300px;height:300px;margin:110px auto 0;border-width:10px;box-shadow:0 0 0 12px {line}}}
.end .big{{font-size:120px;margin-top:56px}} .end .cta{{font-weight:900;font-size:64px;margin-top:40px;color:{sig if sigtext!='#FFFFFF' else '#fff'}}}
.end .h{{font-weight:800;font-size:46px;margin-top:22px;opacity:.9}}
"""
    def chrome(i):
        return (f'<div class="rail" style="width:{1080*i/n:.0f}px"></div>'
                f'<div class="top"><div class="tav"></div><div class="mark">MarlonDecoded</div><div class="ser">{html.escape(spec.get("series",""))}</div></div>'
                f'<div class="cnt">{i}/{n}</div>')
    parts = []
    parts.append(f'<div class="s ct"><div class="in">{chrome(1)}<div class="big">{md(spec["title"])}</div><div class="hook">{md(spec.get("hook",""))}</div></div><div class="deco">{{ }}</div><div class="stack">{"".join(f'<i>{k+1:02d}</i>  {html.escape(re.sub(r"[*`]","",sl["heading"]))}<br>' for k,sl in enumerate(slides))}</div><div class="swipe">SWIPE →</div></div>')
    for k, sl in enumerate(slides):
        i = k + 2
        b = f'<div class="body">{md(sl.get("body",""))}</div>' if sl.get("body") else ""
        c = f'<pre>{code_html(sl["code"])}</pre>' if sl.get("code") else ""
        nt = f'<div class="note">{md(sl["note"])}</div>' if sl.get("note") else ""
        parts.append(f'<div class="s"><div class="in">{chrome(i)}<div class="num">{k+1:02d}</div><h2>{md(sl["heading"])}</h2>{b}{c}{nt}</div></div>')
    parts.append(f'<div class="s end"><div class="in">{chrome(n)}<div class="bav"></div><div class="big">Java,<br><span class="hl">decoded</span> daily.</div><div class="cta">{md(spec.get("cta","Save this 💾"))}</div><div class="h">Follow @marlondecoded</div></div></div>')
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{"".join(parts)}</body></html>'
def main():
    spec = json.load(open(sys.argv[1])); outd = sys.argv[2]; os.makedirs(outd, exist_ok=True)
    duotone(PAL[spec.get("palette","cobalt")][2], "#FFFFFF", os.path.join(HERE,"_av.png")); page_html = build(spec); tmp = os.path.join(HERE, "_page.html"); open(tmp, "w").write(page_html)
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--allow-file-access-from-files"]); pg = b.new_page(viewport={"width":1080,"height":1350})
        pg.goto("file://" + tmp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(400)
        els = pg.query_selector_all(".s")
        for i, el in enumerate(els, 1):
            el.screenshot(path=os.path.join(outd, f"{spec['slug']}-{i:02d}.png"))
        b.close()
    os.remove(tmp); os.remove(os.path.join(HERE,"_av.png"))
    print(len(els), "slides")
main()
