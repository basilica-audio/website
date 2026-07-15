# Basilica Audio — Product Website

Static product site for the Basilica Audio plugin suite — thirteen
sacred-architecture DSP plugins for heavy music. Zero frameworks, zero
external dependencies: a small Python (stdlib-only) generator renders an
overview page plus one product page per plugin.

Deployed via GitHub Pages on every push to `main`
(`.github/workflows/pages.yml` builds `dist/` and publishes it — `dist/` is
never committed).

## Structure

```
build.py                  Generator + internal link checker (python3 stdlib only)
data/plugins.json         All plugin content: names, roles, taglines, features, media
templates/base.html       Page shell (header, footer)
templates/index.html      Overview page (hero + card grid)
templates/plugin.html     Product page (about, features, downloads, stubs, links)
assets/css/style.css      Suite stylesheet (charcoal + antique gold, system fonts)
assets/js/releases.js     Client-side latest-release download buttons
assets/icons/<slug>.png   Plugin icons (256 px)
assets/org.png            Org emblem (512 px)
dist/                     Build output (gitignored, built in CI)
```

## Local preview

```sh
python3 build.py
python3 -m http.server -d dist
# open http://localhost:8000
```

`build.py` fails the build if any generated page contains a broken internal
link, so a green build means the site is internally consistent.

## Configuration

The GitHub org login lives in **one** place: the `ORG` constant at the top of
`build.py`. Templates and the client-side release fetcher (via
`<body data-org="...">`) both receive it from there. When the org is renamed
from `metal-up-your-ass` to `basilica-audio`, change only that constant and
rebuild.

## Downloads

Each product page ships with a static fallback link to the plugin's GitHub
releases page. On load, `assets/js/releases.js` queries
`https://api.github.com/repos/<ORG>/<Repo>/releases/latest` and replaces the
fallback with one styled button per `.zip` asset (platform, version, size,
publish date). If the API call fails — offline, rate-limited, no release yet —
the fallback link simply stays.

## Adding screenshots and audio examples later

Product pages render honest "coming with the next release" empty states until
real media exists. To populate them for a plugin:

1. Drop files into `assets/<slug>/` (create the directory), e.g.
   `assets/requiem/main-window.png` or `assets/requiem/choir-before-after.mp3`.
   - Screenshots: `.png` `.jpg` `.jpeg` `.webp` `.gif`
   - Audio: `.mp3` `.wav` `.ogg` `.flac` `.m4a`
2. Rebuild. That's it — the template auto-discovers the files (sorted by
   name; captions derived from the filename, `main-window.png` → "Main window").
3. Optional: curate order and captions explicitly in `data/plugins.json`:

   ```json
   {
     "slug": "requiem",
     "screenshots": [
       { "file": "main-window.png", "caption": "The main window" }
     ],
     "audio": [
       { "file": "choir-before-after.mp3", "caption": "Choir bus, before/after" }
     ]
   }
   ```

   When these fields exist they take precedence over auto-discovery.

## Donations

The "Support development" section is a deliberate stub: visually present,
buttons disabled, no real payment links. Wire up GitHub Sponsors / Ko-fi /
PayPal in `templates/plugin.html` (see the HTML comment there) when the
accounts exist.

## License

The website sources are part of the Basilica Audio suite. All plugins are
licensed under the GNU AGPL-3.0.
