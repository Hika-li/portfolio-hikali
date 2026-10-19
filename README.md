# sabri-mohamadi.fr

Portfolio site and CVs for Sabri Mohamadi, Producer & Game Designer (Tokyo).

- `src/`: page templates (`index.html`, `contact.html`), all texts in `i18n.json` (EN / JA / FR) and `build.py`.
  Run `python3 src/build.py` after any text or template change: it writes one real page per language into `docs/` (English at `/`, Japanese at `/ja/`, French at `/fr/`) plus `sitemap.xml`.
- `docs/`: the generated site served by GitHub Pages (styles, scripts, images, CV PDFs, 404 page).
- `cv/`: HTML sources for the CV (EN) and 職務経歴書 (JA). Run `node cv/build.mjs` to regenerate the PDFs into `docs/assets/cv/`.
- `meishi/`: business cards source; `node meishi/build.mjs` writes the print PDF.
