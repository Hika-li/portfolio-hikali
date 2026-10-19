"""Builds the static site in docs/ from the templates in src/.

One page per language: English at the root, Japanese in /ja/, French in /fr/.
Every element with data-i18n="key" gets its text from src/i18n.json, so each
language is real HTML that search engines can index (no client-side swap).

Usage: python3 src/build.py
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
OUT = ROOT / "docs"
SITE = "https://www.sabri-mohamadi.fr"
LANGS = {"en": "", "ja": "ja/", "fr": "fr/"}
LABELS = {"en": "EN", "ja": "日本語", "fr": "FR"}
PAGES = {"index.html": "", "contact.html": "contact.html"}

data = json.loads((SRC / "i18n.json").read_text(encoding="utf-8"))


def page_url(lang, page):
    return f"{SITE}/{LANGS[lang]}{PAGES[page]}"


def relink(s, prefix):
    """Point local src/href attributes at the site root from a language subfolder."""
    if not prefix:
        return s

    def fix(m):
        attr, url = m.group(1), m.group(2)
        if re.match(r"(https?:|mailto:|#|/|data:)", url):
            return m.group(0)
        if url.startswith(("index.html", "contact.html")):
            return m.group(0)
        return f'{attr}="{prefix}{url}"'

    def fix_srcset(m):
        parts = [p.strip() for p in m.group(1).split(",")]
        return 'srcset="' + ", ".join(p if re.match(r"(https?:|/|data:)", p) else prefix + p for p in parts) + '"'

    s = re.sub(r'\bsrcset="([^"]*)"', fix_srcset, s)
    return re.sub(r'\b(src|href)="([^"]*)"', fix, s)


def render(page, lang):
    s = (SRC / page).read_text(encoding="utf-8")
    t, meta = data[lang], data["meta"][lang]

    s = re.sub(
        r'(<(\w+)[^>]*\sdata-i18n="([^"]+)"[^>]*>)(.*?)(</\2>)',
        lambda m: m.group(1) + t[m.group(3)] + m.group(5),
        s,
        flags=re.S,
    )
    s = re.sub(r"\{\{t:([\w.]+)\}\}", lambda m: html.escape(t[m.group(1)], quote=True), s)

    is_contact = page == "contact.html"
    hreflang = "\n".join(
        f'<link rel="alternate" hreflang="{l}" href="{page_url(l, page)}">' for l in LANGS
    ) + f'\n<link rel="alternate" hreflang="x-default" href="{page_url("en", page)}">'
    langlinks = "".join(
        f'<a href="/{LANGS[l]}{PAGES[page]}" hreflang="{l}" lang="{l}"'
        + (' aria-current="true"' if l == lang else "")
        + f">{LABELS[l]}</a>"
        for l in LANGS
    )
    s = (
        s.replace("{{TITLE}}", html.escape(meta["ctitle"] if is_contact else meta["title"], quote=True))
        .replace("{{DESC}}", html.escape(meta["cdesc"] if is_contact else meta["desc"], quote=True))
        .replace("{{URL}}", page_url(lang, page))
        .replace("{{LOCALE}}", meta["locale"])
        .replace("{{HREFLANG}}", hreflang)
        .replace("{{LANGLINKS}}", langlinks)
    )
    s = s.replace('<html lang="en">', f'<html lang="{lang}">', 1)
    s = relink(s, "../" if LANGS[lang] else "")
    assert "{{" not in s, f"unfilled placeholder in {lang}/{page}"
    return s


for lang, sub in LANGS.items():
    for page in PAGES:
        dest = OUT / sub / page
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(render(page, lang), encoding="utf-8")
        print("wrote", dest.relative_to(ROOT))

urls = []
for page in PAGES:
    alts = "".join(
        f'\n    <xhtml:link rel="alternate" hreflang="{l}" href="{page_url(l, page)}"/>' for l in LANGS
    )
    for lang in LANGS:
        urls.append(f"  <url>\n    <loc>{page_url(lang, page)}</loc>{alts}\n  </url>")
(OUT / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
    + "\n".join(urls)
    + "\n</urlset>\n",
    encoding="utf-8",
)
print("wrote docs/sitemap.xml")
