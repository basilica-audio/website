#!/usr/bin/env python3
"""Static site generator for the Basilica Audio product website.

Python 3 standard library only. Reads data/plugins.json and templates/,
writes the finished site to dist/ (overview page + one product page per
plugin), copies assets, and link-checks every generated HTML file.

Usage:
    python3 build.py
"""
from __future__ import annotations

import html
import json
import re
import shutil
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"

# ---------------------------------------------------------------------------
# Site configuration
# ---------------------------------------------------------------------------
# GitHub org login — SINGLE SOURCE OF TRUTH for the whole site (templates and
# the client-side release fetcher both receive it from here). When the org is
# renamed from "metal-up-your-ass" to "basilica-audio", change ONLY this line.
ORG = "basilica-audio"

SITE_NAME = "Basilica Audio"
SITE_TAGLINE = "Eleven sacred-architecture DSP plugins for heavy music"

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
AUDIO_EXTS = {".mp3", ".wav", ".ogg", ".flac", ".m4a"}
AUDIO_MIME = {
    ".mp3": "audio/mpeg", ".wav": "audio/wav", ".ogg": "audio/ogg",
    ".flac": "audio/flac", ".m4a": "audio/mp4",
}

PLACEHOLDER_RE = re.compile(r"\{\{[a-z_]+\}\}")


def render(template: str, context: dict) -> str:
    """Minimal {{placeholder}} substitution with a leftover-placeholder guard."""
    out = template
    for key, value in context.items():
        out = out.replace("{{" + key + "}}", str(value))
    leftover = PLACEHOLDER_RE.findall(out)
    if leftover:
        raise SystemExit(f"error: unresolved template placeholders: {sorted(set(leftover))}")
    return out


def read_template(name: str) -> str:
    return (ROOT / "templates" / name).read_text(encoding="utf-8")


def feature_item(feature: str) -> str:
    """Render one feature bullet; a leading 'Lead — rest' gets a <strong> lead."""
    if " — " in feature:
        lead, rest = feature.split(" — ", 1)
        return (f"    <li><strong>{html.escape(lead)}</strong> — "
                f"{html.escape(rest)}</li>")
    return f"    <li>{html.escape(feature)}</li>"


def caption_from_filename(path: Path) -> str:
    return path.stem.replace("_", " ").replace("-", " ").strip().capitalize()


def collect_media(plugin: dict, exts: set[str], field: str) -> list[tuple[str, str]]:
    """Return [(relative-file-path-under-assets/<slug>/, caption), ...].

    Sources, in order of precedence:
      1. plugins.json field (list of {"file": ..., "caption": ...}) — files
         resolved against assets/<slug>/, silently skipped if missing.
      2. Auto-discovery: every matching file in assets/<slug>/, sorted.
    """
    slug = plugin["slug"]
    media_dir = ROOT / "assets" / slug
    entries = plugin.get(field)
    found: list[tuple[str, str]] = []
    if isinstance(entries, list):
        for entry in entries:
            name = entry.get("file", "")
            file = media_dir / name
            if file.is_file() and file.suffix.lower() in exts:
                found.append((name, entry.get("caption") or caption_from_filename(file)))
    elif media_dir.is_dir():
        for file in sorted(media_dir.iterdir()):
            if file.is_file() and file.suffix.lower() in exts:
                found.append((file.name, caption_from_filename(file)))
    return found


def screenshots_section(plugin: dict) -> str:
    shots = collect_media(plugin, IMAGE_EXTS, "screenshots")
    if not shots:
        return """<section class="section" aria-labelledby="screenshots-heading">
  <h2 id="screenshots-heading">Screenshots</h2>
  <div class="empty-state">
    <span class="empty-glyph" aria-hidden="true">&#9672;</span>
    <p>Coming with the next release.</p>
    <p class="empty-sub">The custom interface is currently in design —
    screenshots will appear here as soon as it ships.</p>
  </div>
</section>"""
    figures = "\n".join(
        f"""    <figure>
      <img src="../assets/{plugin['slug']}/{html.escape(name)}" alt="{html.escape(caption)}" loading="lazy">
      <figcaption>{html.escape(caption)}</figcaption>
    </figure>"""
        for name, caption in shots
    )
    return f"""<section class="section" aria-labelledby="screenshots-heading">
  <h2 id="screenshots-heading">Screenshots</h2>
  <div class="shot-grid">
{figures}
  </div>
</section>"""


def audio_section(plugin: dict) -> str:
    clips = collect_media(plugin, AUDIO_EXTS, "audio")
    if not clips:
        return """<section class="section" aria-labelledby="audio-heading">
  <h2 id="audio-heading">Audio examples</h2>
  <div class="empty-state">
    <span class="empty-glyph" aria-hidden="true">&#9835;</span>
    <p>Coming with the next release.</p>
    <p class="empty-sub">Before/after clips are being recorded —
    audio examples will appear here with an upcoming release.</p>
  </div>
</section>"""
    items = "\n".join(
        f"""    <li>
      <span class="audio-caption">{html.escape(caption)}</span>
      <audio controls preload="none"
             src="../assets/{plugin['slug']}/{html.escape(name)}">
        <a href="../assets/{plugin['slug']}/{html.escape(name)}">Download {html.escape(caption)}</a>
      </audio>
    </li>"""
        for name, caption in clips
    )
    return f"""<section class="section" aria-labelledby="audio-heading">
  <h2 id="audio-heading">Audio examples</h2>
  <ul class="audio-list">
{items}
  </ul>
</section>"""


def build_card(plugin: dict) -> str:
    slug, name, role = plugin["slug"], plugin["name"], plugin["role"]
    return f"""  <article class="card">
    <img class="card-icon" src="assets/icons/{slug}.png" alt="" width="92" height="92">
    <h2><a class="card-link" href="{slug}/index.html">{html.escape(name)}</a></h2>
    <p class="card-role">{html.escape(role)}</p>
    <p class="card-actions">
      <span class="details-hint" aria-hidden="true">Details&nbsp;&rarr;</span>
      <a href="{slug}/index.html#download">Download</a>
    </p>
  </article>"""


def build_site() -> None:
    data = json.loads((ROOT / "data" / "plugins.json").read_text(encoding="utf-8"))
    plugins = data["plugins"]
    required = {"slug", "name", "repo", "role", "tagline", "description", "features"}
    for plugin in plugins:
        missing = required - plugin.keys()
        if missing:
            raise SystemExit(f"error: plugin {plugin.get('slug', '?')} missing keys: {sorted(missing)}")

    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)

    # Assets (icons, emblem, css, js, and any per-plugin media directories).
    shutil.copytree(ROOT / "assets", DIST / "assets")

    base = read_template("base.html")
    index_tpl = read_template("index.html")
    plugin_tpl = read_template("plugin.html")

    # Overview page.
    cards = "\n".join(build_card(p) for p in plugins)
    index_content = render(index_tpl, {"site_tagline": html.escape(SITE_TAGLINE), "cards": cards})
    (DIST / "index.html").write_text(render(base, {
        "title": f"{SITE_NAME} — {SITE_TAGLINE}",
        "description": (f"{SITE_TAGLINE}. Free and open-source AU/VST3/Standalone "
                        "plugins for macOS and Windows, licensed AGPL-3.0."),
        "root": "",
        "org": ORG,
        "content": index_content,
    }), encoding="utf-8")

    # Product pages.
    for plugin in plugins:
        note = plugin.get("note")
        note_html = f'<p class="rename-note">{html.escape(note)}</p>' if note else ""
        features = "\n".join(feature_item(f) for f in plugin["features"])
        content = render(plugin_tpl, {
            "slug": plugin["slug"],
            "name": html.escape(plugin["name"]),
            "repo": plugin["repo"],
            "role": html.escape(plugin["role"]),
            "tagline": html.escape(plugin["tagline"]),
            "description": html.escape(plugin["description"]),
            "note": note_html,
            "features": features,
            "org": ORG,
            "screenshots_section": screenshots_section(plugin),
            "audio_section": audio_section(plugin),
        })
        page_dir = DIST / plugin["slug"]
        page_dir.mkdir()
        (page_dir / "index.html").write_text(render(base, {
            "title": f"{plugin['name']} — {plugin['role']} | {SITE_NAME}",
            "description": html.escape(plugin["tagline"]),
            "root": "../",
            "org": ORG,
            "content": content,
        }), encoding="utf-8")

    print(f"built {1 + len(plugins)} pages -> {DIST}")


# ---------------------------------------------------------------------------
# Link check
# ---------------------------------------------------------------------------
class RefCollector(HTMLParser):
    ATTRS = {"href", "src"}

    def __init__(self) -> None:
        super().__init__()
        self.refs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list) -> None:
        for name, value in attrs:
            if name in self.ATTRS and value:
                self.refs.append(value)


def check_links() -> None:
    broken: list[str] = []
    for page in sorted(DIST.rglob("*.html")):
        collector = RefCollector()
        collector.feed(page.read_text(encoding="utf-8"))
        for ref in collector.refs:
            parsed = urlparse(ref)
            if parsed.scheme or ref.startswith(("#", "mailto:")):
                continue  # external / fragment-only — not checked here
            path = parsed.path
            if not path:
                continue
            target = (page.parent / path).resolve()
            if path.endswith("/"):
                target = target / "index.html"
            if not target.exists():
                broken.append(f"{page.relative_to(DIST)}: {ref}")
    if broken:
        print("BROKEN internal links:", file=sys.stderr)
        for item in broken:
            print(f"  {item}", file=sys.stderr)
        raise SystemExit(1)
    print("link check passed: no broken internal links")


if __name__ == "__main__":
    build_site()
    check_links()
