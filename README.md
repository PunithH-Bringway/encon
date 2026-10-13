# Encon Engineering Solutions — website

Static site (HTML/CSS/JS, no dependencies) for Encon Engineering Solutions, Bengaluru: water, sewage and wastewater treatment & recycle systems.

- `src/` — page bodies (edit these)
- `build.py` — shared header/footer/icons, contact details and the projects list; run `python build.py` to regenerate `site/`
- `site/` — the deployable website (upload this folder to hosting)

Preview locally: `python -m http.server 8090 --directory site`
