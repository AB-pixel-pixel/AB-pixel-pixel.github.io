# Shaobin Ling · Personal Homepage

Bilingual academic homepage for Shaobin Ling (凌绍彬). English by default, with a Chinese language switch.

## Features

- Research interests, six publications, education, experience, and honors.
- First-author filter and expandable contributions.
- Local research demo videos and links to papers and project pages.
- Responsive layout; no frontend dependencies or external font/CDN requests.

## Edit content

Edit `data/content.json`, then regenerate and validate:

```sh
python3 scripts/build.py
python3 scripts/check.py
```

Styles: `assets/style.css`. Interactions: `assets/main.js`.

## Preview

```sh
python3 -m http.server 4173 --bind 127.0.0.1
```

Open http://127.0.0.1:4173/ or open `index.html` directly.

## Deploy

Use GitHub Pages with **GitHub Actions** as the source. The included workflow generates, validates, and deploys the site on pushes to `main`.

Only the homepage and its assets are deployed. No public résumé is included.

## Design references

Original implementation inspired by the publication-focused organization of [Jon Barron](https://jonbarron.info/), [Shuran Song](https://shurans.github.io/), and [Deepak Pathak](https://www.cs.cmu.edu/~dpathak/).

Research figures, photographs, and videos retain their original rights.
