#!/usr/bin/env python3
"""Static site generator for the Basilica Audio product website.

Python 3 standard library only. Reads data/plugins.json and templates/,
writes the finished site to dist/ — a bilingual (English + German) tree:
overview page + one product page per plugin + one user-manual page per
plugin (where a manual exists), each mirrored under /de/. Copies assets,
and link-checks every generated HTML file.

Usage:
    python3 build.py
"""
from __future__ import annotations

import html
import json
import posixpath
import re
import shutil
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

import lib_md

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

# Absolute site base — canonical URLs, hreflang alternates, Open Graph
# metadata, the sitemap and the 404 page's links all derive from this one
# constant (hreflang/canonical URLs must be fully qualified per Google's
# documentation, so relative links are not an option there).
BASE_URL = "https://basilica-audio.github.io/website/"

# The pre-composed 1200x630 Open Graph card (assets/og-card.png) shared by
# every page — scrapers do not follow relative URLs, hence BASE_URL.
OG_IMAGE = {"file": "assets/og-card.png", "width": 1200, "height": 630}

OG_LOCALES = {"en": "en_GB", "de": "de_DE"}

LANGS = ("en", "de")

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
AUDIO_EXTS = {".mp3", ".wav", ".ogg", ".flac", ".m4a"}
AUDIO_MIME = {
    ".mp3": "audio/mpeg", ".wav": "audio/wav", ".ogg": "audio/ogg",
    ".flac": "audio/flac", ".m4a": "audio/mp4",
}

PLACEHOLDER_RE = re.compile(r"\{\{[a-z_]+\}\}")

# Compatible-DAW logo strip, rendered on every product page and on the
# overview page. Keys map to assets/daws/daw-<key>.webp. Pro Tools is
# deliberately absent: it only loads AAX plugins, which the suite does not
# ship (its logo tile sits unused in assets/daws/ alongside the others).
DAWS = [
    ("cubase", "Cubase"),
    ("reaper", "REAPER"),
    ("logic-pro", "Logic Pro"),
    ("ableton-live", "Ableton Live"),
    ("studio-one", "Studio One"),
    ("fl-studio", "FL Studio"),
    ("reason", "Reason"),
]

MANUALS_DIR = ROOT / "data" / "manuals"
GUIDES_DIR = ROOT / "data" / "guides"

# ---------------------------------------------------------------------------
# UI chrome strings — every piece of site chrome (nav, buttons, empty
# states, footer, manual scaffolding, ...) lives here. Plugin CONTENT
# (name, role, tagline, description, features) comes from plugins.json and
# is translated separately (see the "de" object in that schema); this dict
# is only ever chrome. DSP/product terms are deliberately left in English
# even in the German column (Mix, Bypass, Threshold, dB, plugin format
# names, etc.) — that's how German-speaking audio engineers talk.
# ---------------------------------------------------------------------------
STRINGS = {
    "en": {
        "html_lang": "en",
        "brand_name": "Basilica Audio",
        "skip_link": "Skip to content",
        "nav_plugins": "Plugins",
        "nav_github": "GitHub",
        "lang_switch_label": "Language",
        "site_tagline": "Thirteen sacred-architecture DSP plugins for heavy music",
        "site_description": ("Thirteen sacred-architecture DSP plugins for heavy music. "
                              "Free and open-source AU/VST3/Standalone plugins for macOS "
                              "and Windows, licensed AGPL-3.0."),
        "hero_sub": ("Free &amp; open-source audio plugins — AU · VST3 · Standalone, "
                     "for macOS and Windows, licensed under the GNU AGPL-3.0."),
        "emblem_alt": "Basilica Audio emblem",
        "all_plugins": "All plugins",
        "details_hint": "Details",
        "download_label": "Download",
        "formats_line": "AU · VST3 · Standalone&ensp;·&ensp;macOS &amp; Windows&ensp;·&ensp;AGPL-3.0",
        "about_heading": "About",
        "lore_heading": "Why the name?",
        "engineering_heading": "Under the hood",
        "signed_note": ("The macOS binaries are Developer-ID-signed, notarised by Apple "
                        "and stapled — they install and open without Gatekeeper warnings. "
                        "Windows builds are not yet Authenticode-signed; SmartScreen may "
                        "warn about an unknown publisher."),
        "features_heading": "Features",
        "download_heading": "Download",
        "download_fallback": "The latest builds are published on {link}.",
        "download_fallback_link": "GitHub&nbsp;Releases",
        "screenshots_heading": "Screenshots",
        "screenshots_empty": "Coming with the next release.",
        "screenshots_empty_sub": ("The custom interface is currently in design — "
                                   "screenshots will appear here as soon as it ships."),
        "mockup_caption": "product mockup",
        "screenshot_caption": "screenshot",
        "audio_heading": "Audio examples",
        "audio_empty": "Coming with the next release.",
        "audio_empty_sub": ("Before/after clips are being recorded — audio examples will "
                             "appear here with an upcoming release."),
        "audio_download_prefix": "Download {caption}",
        "daws_heading": "Compatible DAWs",
        "daws_note": ("Any modern DAW that supports VST3 or Audio Units. "
                       "Pro Tools (AAX) is currently not supported."),
        "support_heading": "Support development",
        "support_body": ("Basilica Audio is free software, built at night and tuned by "
                          "ear. If it earns a place in your session, you can help keep "
                          "the candles lit."),
        "donate_note": "Donation links are not wired up yet — they will go live soon.",
        "links_heading": "Links",
        "link_source": "Source code on GitHub",
        "link_manual": "User manual",
        "link_manual_other_lang_hint": " (English)",
        "link_releases": "All releases",
        "link_license": "License — GNU AGPL-3.0",
        "release_notes_label": "Release notes & previous versions",
        "footer_note": ("Free and open-source software under the GNU AGPL-3.0. "
                         "macOS binaries are Developer-ID-signed and notarised."),
        "manual_back": "Back to {name}",
        "manual_title_suffix": "User manual",
        "manual_description": "User manual for {name} — {site_name}.",
        "nav_guides": "Guides",
        "guide_label": "How-to guide",
        "guide_description": "Practical settings guide for {name} — {site_name}.",
        "signal_chain_title": "Signal chain guide",
        "signal_chain_description": ("How the thirteen Basilica Audio plugins fit together in a "
                                      "heavy-music production — guitars, bass, buses, mastering, "
                                      "vocals & choir, and space."),
        "signal_chain_callout": "Read the signal-chain guide",
    },
    "de": {
        "html_lang": "de",
        "brand_name": "Basilica Audio",
        "skip_link": "Zum Inhalt springen",
        "nav_plugins": "Plugins",
        "nav_github": "GitHub",
        "lang_switch_label": "Sprache",
        "site_tagline": "Dreizehn DSP-Plugins in sakraler Architektur für Heavy Music",
        "site_description": ("Dreizehn DSP-Plugins in sakraler Architektur für schwere "
                              "Musik. Kostenlose Open-Source-Plugins (AU/VST3/Standalone) "
                              "für macOS und Windows, lizenziert unter AGPL-3.0."),
        "hero_sub": ("Kostenlose Open-Source-Audio-Plugins — AU · VST3 · Standalone, "
                     "für macOS und Windows, lizenziert unter der GNU AGPL-3.0."),
        "emblem_alt": "Basilica-Audio-Emblem",
        "all_plugins": "Alle Plugins",
        "details_hint": "Details",
        "download_label": "Download",
        "formats_line": "AU · VST3 · Standalone&ensp;·&ensp;macOS &amp; Windows&ensp;·&ensp;AGPL-3.0",
        "about_heading": "Über dieses Plugin",
        "lore_heading": "Woher der Name?",
        "engineering_heading": "Unter der Haube",
        "signed_note": ("Die macOS-Binaries sind Developer-ID-signiert, von Apple "
                        "notarisiert und gestapelt — sie installieren und öffnen ohne "
                        "Gatekeeper-Warnung. Windows-Builds sind noch nicht "
                        "Authenticode-signiert; SmartScreen warnt eventuell vor einem "
                        "unbekannten Herausgeber."),
        "features_heading": "Funktionen",
        "download_heading": "Download",
        "download_fallback": "Die aktuellen Builds werden auf {link} veröffentlicht.",
        "download_fallback_link": "GitHub&nbsp;Releases",
        "screenshots_heading": "Screenshots",
        "screenshots_empty": "Kommt mit dem nächsten Release.",
        "screenshots_empty_sub": ("Die individuelle Oberfläche befindet sich aktuell in "
                                   "der Gestaltung — Screenshots erscheinen hier, sobald "
                                   "sie fertig ist."),
        "mockup_caption": "Produkt-Mockup",
        "screenshot_caption": "Screenshot",
        "audio_heading": "Hörbeispiele",
        "audio_empty": "Kommt mit dem nächsten Release.",
        "audio_empty_sub": ("Vorher/Nachher-Clips werden gerade aufgenommen — "
                             "Hörbeispiele erscheinen hier mit einem kommenden Release."),
        "audio_download_prefix": "{caption} herunterladen",
        "daws_heading": "Kompatible DAWs",
        "daws_note": ("Jede moderne DAW mit VST3- oder Audio-Units-Unterstützung. "
                       "Pro Tools (AAX) wird derzeit nicht unterstützt."),
        "support_heading": "Entwicklung unterstützen",
        "support_body": ("Basilica Audio ist freie Software, nachts gebaut und nach "
                          "Gehör abgestimmt. Wenn sie sich einen Platz in deiner Session "
                          "verdient, kannst du helfen, die Kerzen am Brennen zu halten."),
        "donate_note": "Spenden-Links sind noch nicht verknüpft — sie werden in Kürze freigeschaltet.",
        "links_heading": "Links",
        "link_source": "Quellcode auf GitHub",
        "link_manual": "Bedienungsanleitung",
        "link_manual_other_lang_hint": " (Englisch)",
        "link_releases": "Alle Releases",
        "link_license": "Lizenz — GNU AGPL-3.0",
        "release_notes_label": "Release-Notes & frühere Versionen",
        "footer_note": ("Freie und quelloffene Software unter der GNU AGPL-3.0. "
                         "macOS-Binaries sind Developer-ID-signiert und notarisiert."),
        "manual_back": "Zurück zu {name}",
        "manual_title_suffix": "Bedienungsanleitung",
        "manual_description": "Bedienungsanleitung für {name} — {site_name}.",
        "nav_guides": "Guides",
        "guide_label": "Praxis-Guide",
        "guide_description": "Praxis-Guide mit Einstellungsempfehlungen für {name} — {site_name}.",
        "signal_chain_title": "Signalketten-Guide",
        "signal_chain_description": ("Wie die dreizehn Basilica-Audio-Plugins in einer "
                                      "Heavy-Music-Produktion zusammenspielen — Gitarren, Bass, "
                                      "Busse, Mastering, Vocals & Chor und Raum."),
        "signal_chain_callout": "Signalketten-Guide lesen",
    },
}

# The root-index-only redirect: if the visitor's stored/browser language is
# German, bounce them to /de/ before the English page paints. Uses a
# page-relative URL ("de/") so the site stays relocatable under any deploy
# path prefix (GitHub Pages project sites are served under /<repo>/).
ROOT_REDIRECT_SCRIPT = """<script>
(function () {
  try {
    var stored = localStorage.getItem("lang");
    var wantsDe = stored === "de" || (!stored && /^de/i.test(navigator.language || ""));
    if (wantsDe) { window.location.replace("de/"); }
  } catch (e) { /* localStorage/navigator unavailable — stay on English */ }
})();
</script>
"""

# Strips the generated-from HTML comment lib_md sync prepends to each
# data/manuals/<slug>.<lang>.md file (see README.md's "Manual sync" section).
_GENERATED_COMMENT_RE = re.compile(r"^<!--.*?-->\s*\n+", re.DOTALL)

# Drops a leading standalone "centered icon" paragraph — the GitHub-README
# convention `<p align="center"><img .../></p>` that several plugin repos'
# docs/manual.md files open with. lib_md deliberately escapes raw HTML
# rather than executing it (see lib_md.py's docstring), so left in place
# this would render as ugly escaped tag text; the manual page's breadcrumb
# leads straight back to the product page, which already carries the icon,
# so dropping it here loses nothing. This only affects the HTML *rendering*
# pass — the stored data/manuals/*.md files stay byte-verbatim from sync.
_LEADING_ICON_RE = re.compile(r"^\s*<p[^>]*>\s*<img[^>]*>\s*</p>\s*\n+", re.IGNORECASE)


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


def loc(plugin: dict, lang: str, key: str):
    """Look up a translatable plugin-content field with English fallback.

    plugins.json may carry an optional "de" object per plugin with any of
    "role"/"tagline"/"description"/"features". Missing object, missing key,
    or lang == "en" all fall back to the top-level English field — the site
    must build correctly before any translations land (binding decision 4).
    """
    if lang != "en":
        de = plugin.get("de")
        if isinstance(de, dict) and key in de:
            return de[key]
    return plugin[key]


# ---------------------------------------------------------------------------
# Path helpers — every page lives at "<dir>/index.html" under dist/, where
# dir is a POSIX-style path relative to dist/ ("" for the site root itself,
# "overture" for a plugin page, "overture/manual" for its manual, "de",
# "de/overture", "de/overture/manual" for the German mirror). These two
# helpers are the only place that needs to know how deep a page is.
# ---------------------------------------------------------------------------
def asset_root(dir_: str) -> str:
    """Relative prefix from a page back up to dist/ (where assets/ lives)."""
    if not dir_:
        return ""
    return "../" * (dir_.count("/") + 1)


def rel_link(from_dir: str, to_dir: str) -> str:
    """Relative href from the page in from_dir to the index.html in to_dir."""
    start = from_dir if from_dir else "."
    target = f"{to_dir}/index.html" if to_dir else "index.html"
    return posixpath.relpath(target, start)


def lang_dir(lang: str, *parts: str) -> str:
    segments = [] if lang == "en" else ["de"]
    segments.extend(parts)
    return "/".join(segments)


def page_url(dir_: str) -> str:
    """Absolute canonical URL of the page living at dist/<dir_>/index.html."""
    return BASE_URL if not dir_ else f"{BASE_URL}{dir_}/"


def image_size(path: Path) -> tuple[int, int] | None:
    """Pixel dimensions of a PNG or WebP file, stdlib-only (no Pillow in CI).

    Supports PNG (IHDR) and all three WebP flavours (VP8X extended header,
    VP8 lossy frame header, VP8L lossless stream header). Returns None for
    anything it cannot parse — callers then simply omit width/height.
    """
    try:
        head = path.read_bytes()[:64]
    except OSError:
        return None
    if head[:8] == b"\x89PNG\r\n\x1a\n" and head[12:16] == b"IHDR":
        return (int.from_bytes(head[16:20], "big"), int.from_bytes(head[20:24], "big"))
    if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
        chunk = head[12:16]
        if chunk == b"VP8X":
            return (int.from_bytes(head[24:27], "little") + 1,
                    int.from_bytes(head[27:30], "little") + 1)
        if chunk == b"VP8 " and head[23:26] == b"\x9d\x01\x2a":
            return (int.from_bytes(head[26:28], "little") & 0x3FFF,
                    int.from_bytes(head[28:30], "little") & 0x3FFF)
        if chunk == b"VP8L" and head[20:21] == b"\x2f":
            bits = int.from_bytes(head[21:25], "little")
            return ((bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1)
    return None


def hreflang_tags(this_dir: str, en_dir: str, de_dir: str) -> str:
    """Fully-qualified alternate links — Google requires absolute URLs here."""
    en_href = page_url(en_dir)
    de_href = page_url(de_dir)
    return (
        f'<link rel="alternate" hreflang="en" href="{en_href}">\n'
        f'<link rel="alternate" hreflang="de" href="{de_href}">\n'
        f'<link rel="alternate" hreflang="x-default" href="{en_href}">'
    )


def seo_head(lang: str, dir_: str, en_dir: str, de_dir: str,
             title: str, description: str, jsonld: str = "") -> str:
    """Canonical + hreflang + Open Graph + Twitter card (+ optional JSON-LD)."""
    url = page_url(dir_)
    esc_title = html.escape(title, quote=True)
    esc_desc = html.escape(description, quote=True)
    locale = OG_LOCALES[lang]
    alt_locale = OG_LOCALES["de" if lang == "en" else "en"]
    lines = [
        hreflang_tags(dir_, en_dir, de_dir),
        f'<link rel="canonical" href="{url}">',
        '<meta property="og:type" content="website">',
        f'<meta property="og:site_name" content="{SITE_NAME}">',
        f'<meta property="og:title" content="{esc_title}">',
        f'<meta property="og:description" content="{esc_desc}">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:image" content="{BASE_URL}{OG_IMAGE["file"]}">',
        f'<meta property="og:image:width" content="{OG_IMAGE["width"]}">',
        f'<meta property="og:image:height" content="{OG_IMAGE["height"]}">',
        f'<meta property="og:image:alt" content="{SITE_NAME}">',
        f'<meta property="og:locale" content="{locale}">',
        f'<meta property="og:locale:alternate" content="{alt_locale}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{esc_title}">',
        f'<meta name="twitter:description" content="{esc_desc}">',
        f'<meta name="twitter:image" content="{BASE_URL}{OG_IMAGE["file"]}">',
    ]
    if jsonld:
        lines.append(f'<script type="application/ld+json">{jsonld}</script>')
    return "\n".join(lines)


def lang_switch_nav(lang: str, this_dir: str, alt_dir: str) -> str:
    """The 'EN | DE' selector every page carries in its header."""
    en_dir = this_dir if lang == "en" else alt_dir
    de_dir = alt_dir if lang == "en" else this_dir
    en_href = rel_link(this_dir, en_dir)
    de_href = rel_link(this_dir, de_dir)
    label = STRINGS[lang]["lang_switch_label"]

    def item(code: str, href: str, active: bool) -> str:
        current = ' aria-current="page"' if active else ""
        cls = " lang-link-active" if active else ""
        return (f'<a class="lang-link{cls}" href="{href}"{current} '
                f'onclick="try{{localStorage.setItem(&quot;lang&quot;,&quot;{code}&quot;)}}'
                f'catch(e){{}}">{code.upper()}</a>')

    return (
        f'<nav class="lang-switch" aria-label="{html.escape(label)}">'
        f'{item("en", en_href, lang == "en")}'
        f'<span aria-hidden="true">|</span>'
        f'{item("de", de_href, lang == "de")}'
        f"</nav>"
    )


def manual_link_rewriter(org: str, repo: str):
    """Rewrite a manual's doc-relative links (e.g. "architecture.md", which
    resolves inside the plugin repo's docs/ folder) to the plugin's GitHub
    source so they stay valid once the manual is hosted on this site."""
    def rewrite(url: str) -> str:
        if url.startswith(("#", "http://", "https://", "mailto:")):
            return url
        return f"https://github.com/{org}/{repo}/blob/main/docs/{url}"
    return rewrite


def load_manual_markdown(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    text = _GENERATED_COMMENT_RE.sub("", text, count=1)
    text = _LEADING_ICON_RE.sub("", text, count=1)
    return text


def manual_path(slug: str, lang: str) -> Path:
    return MANUALS_DIR / f"{slug}.{lang}.md"


def guide_path(slug: str, lang: str) -> Path:
    return GUIDES_DIR / f"{slug}.{lang}.md"


def guides_nav_href(lang: str, dir_: str) -> str:
    """Relative href from any page to that language's signal-chain guide —
    the 'Guides' header nav link (base_context). Unlike nav_plugins/brand
    (which use the depth-only "root" prefix and always land on the English
    tree), this is computed with rel_link so it stays language-correct on
    German pages too."""
    return rel_link(dir_, lang_dir(lang, "signal-chain"))


def home_href(lang: str, dir_: str) -> str:
    """Language-correct relative href to that language's overview page —
    used by the brand/logo link and the Plugins nav link (base_context),
    which previously used the depth-only "root" prefix and therefore always
    landed on the English overview even from German pages."""
    return rel_link(dir_, lang_dir(lang))


# ---------------------------------------------------------------------------
# Page-fragment builders
# ---------------------------------------------------------------------------
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

    Auto-discovery skips the plugin's "mockup" file (if any) for the
    "screenshots" field — that file lives in the same assets/<slug>/
    directory but is rendered separately, with its own caption, by
    mockup_figure()/screenshots_section() until real screenshots exist.
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
        mockup = plugin.get("mockup")
        skip = mockup.get("file") if field == "screenshots" and isinstance(mockup, dict) else None
        for file in sorted(media_dir.iterdir()):
            if file.name == skip:
                continue
            if file.is_file() and file.suffix.lower() in exts:
                found.append((file.name, caption_from_filename(file)))
    return found


def media_figure(src: str, file: Path, caption: str) -> str:
    """One gallery <figure> — explicit width/height (read from the image
    header, stdlib-only) so lazy-loaded galleries reserve their box and
    never shift layout."""
    size = image_size(file)
    dims = f' width="{size[0]}" height="{size[1]}"' if size else ""
    return f"""    <figure>
      <img src="{html.escape(src)}" alt="{html.escape(caption)}"{dims} loading="lazy" decoding="async">
      <figcaption>{html.escape(caption)}</figcaption>
    </figure>"""


def mockup_figure(plugin: dict, lang: str, root: str) -> str | None:
    """A single-image fallback for the Screenshots section: plugins.json may
    carry an optional "mockup" object ({"file": ..., "is_screenshot": bool})
    pointing at a file under assets/<slug>/. Used only until real screenshots
    (auto-discovered or listed in the "screenshots" field) exist for that
    plugin — see screenshots_section. "is_screenshot" is true for the one
    plugin (Silentium) whose mockup file is already its real, approved GUI;
    every other plugin's mockup is an early marketing render of the planned
    faceplate, captioned accordingly so it's never mistaken for a screenshot
    of a finished, ready plugin."""
    s = STRINGS[lang]
    mockup = plugin.get("mockup")
    if not isinstance(mockup, dict) or not mockup.get("file"):
        return None
    slug = plugin["slug"]
    name = mockup["file"]
    if not (ROOT / "assets" / slug / name).is_file():
        return None
    caption = s["screenshot_caption"] if mockup.get("is_screenshot") else s["mockup_caption"]
    return media_figure(f"{root}assets/{slug}/{name}", ROOT / "assets" / slug / name, caption)


def screenshots_section(plugin: dict, lang: str, root: str) -> str:
    s = STRINGS[lang]
    shots = collect_media(plugin, IMAGE_EXTS, "screenshots")
    if not shots:
        figure = mockup_figure(plugin, lang, root)
        if figure:
            return f"""<section class="section" aria-labelledby="screenshots-heading">
  <h2 id="screenshots-heading">{s['screenshots_heading']}</h2>
  <div class="shot-grid">
{figure}
  </div>
</section>"""
        return f"""<section class="section" aria-labelledby="screenshots-heading">
  <h2 id="screenshots-heading">{s['screenshots_heading']}</h2>
  <div class="empty-state">
    <span class="empty-glyph" aria-hidden="true">&#9672;</span>
    <p>{s['screenshots_empty']}</p>
    <p class="empty-sub">{s['screenshots_empty_sub']}</p>
  </div>
</section>"""
    figures = "\n".join(
        media_figure(f"{root}assets/{plugin['slug']}/{name}",
                     ROOT / "assets" / plugin["slug"] / name, caption)
        for name, caption in shots
    )
    return f"""<section class="section" aria-labelledby="screenshots-heading">
  <h2 id="screenshots-heading">{s['screenshots_heading']}</h2>
  <div class="shot-grid">
{figures}
  </div>
</section>"""


def audio_section(plugin: dict, lang: str, root: str) -> str:
    s = STRINGS[lang]
    clips = collect_media(plugin, AUDIO_EXTS, "audio")
    if not clips:
        return f"""<section class="section" aria-labelledby="audio-heading">
  <h2 id="audio-heading">{s['audio_heading']}</h2>
  <div class="empty-state">
    <span class="empty-glyph" aria-hidden="true">&#9835;</span>
    <p>{s['audio_empty']}</p>
    <p class="empty-sub">{s['audio_empty_sub']}</p>
  </div>
</section>"""
    items = "\n".join(
        f"""    <li>
      <span class="audio-caption">{html.escape(caption)}</span>
      <audio controls preload="none"
             src="{root}assets/{plugin['slug']}/{html.escape(name)}">
        <a href="{root}assets/{plugin['slug']}/{html.escape(name)}">{html.escape(s['audio_download_prefix'].format(caption=caption))}</a>
      </audio>
    </li>"""
        for name, caption in clips
    )
    return f"""<section class="section" aria-labelledby="audio-heading">
  <h2 id="audio-heading">{s['audio_heading']}</h2>
  <ul class="audio-list">
{items}
  </ul>
</section>"""


def daws_section(lang: str, root: str, centered: bool = False) -> str:
    """The compatible-DAWs logo strip (product pages + overview page)."""
    s = STRINGS[lang]
    tiles = "\n".join(
        f'    <li><img src="{root}assets/daws/daw-{key}.webp" alt="{name}" '
        f'title="{name}" width="56" height="56" loading="lazy" decoding="async"></li>'
        for key, name in DAWS
    )
    cls = " daw-section-centered" if centered else ""
    return f"""<section class="section daw-section{cls}" aria-labelledby="daws-heading">
  <h2 id="daws-heading">{s['daws_heading']}</h2>
  <ul class="daw-grid">
{tiles}
  </ul>
  <p class="daw-note">{s['daws_note']}</p>
</section>"""


def build_card(plugin: dict, lang: str, root: str) -> str:
    s = STRINGS[lang]
    slug, name = plugin["slug"], plugin["name"]
    role = loc(plugin, lang, "role")
    return f"""  <article class="card">
    <img class="card-icon" src="{root}assets/icons/{slug}-184.webp" alt="" width="92" height="92" loading="lazy" decoding="async">
    <h2><a class="card-link" href="{slug}/index.html">{html.escape(name)}</a></h2>
    <p class="card-role">{html.escape(role)}</p>
    <p class="card-actions">
      <span class="details-hint" aria-hidden="true">{s['details_hint']}</span>
      <a href="{slug}/index.html#download">{s['download_label']}</a>
    </p>
  </article>"""


def manual_link_item(plugin: dict, lang: str, manuals_present: dict) -> str:
    """The 'User manual' <li> in a product page's Links section, or "" if
    this plugin has no manual in any language (binding decision 5: "its
    manual links must then not render")."""
    s = STRINGS[lang]
    slug = plugin["slug"]
    has_en = manuals_present.get((slug, "en"), False)
    has_de = manuals_present.get((slug, "de"), False)
    if not has_en and not has_de:
        return ""
    this_dir = lang_dir(lang, slug)
    if lang == "en" or has_de:
        target_dir = lang_dir(lang, slug, "manual")
        hint = ""
    else:
        # DE page, no DE manual yet — fall back to the EN manual page.
        target_dir = lang_dir("en", slug, "manual")
        hint = s["link_manual_other_lang_hint"]
    href = rel_link(this_dir, target_dir)
    return f'    <li><a href="{href}">{s["link_manual"]}{hint}</a></li>\n'


def guide_link_item(plugin: dict, lang: str, guides_present: dict) -> str:
    """The 'How-to guide' <li> in a product page's Links section, or "" if
    this plugin has no guide in any language yet — same English-fallback
    convention as manual_link_item above (guides land bilingually per
    batch in practice, but the build must never depend on that)."""
    s = STRINGS[lang]
    slug = plugin["slug"]
    has_en = guides_present.get((slug, "en"), False)
    has_de = guides_present.get((slug, "de"), False)
    if not has_en and not has_de:
        return ""
    this_dir = lang_dir(lang, slug)
    if lang == "en" or has_de:
        target_dir = lang_dir(lang, slug, "guide")
        hint = ""
    else:
        target_dir = lang_dir("en", slug, "guide")
        hint = s["link_manual_other_lang_hint"]
    href = rel_link(this_dir, target_dir)
    return f'    <li><a href="{href}">{s["guide_label"]}{hint}</a></li>\n'


def build_download_fallback(lang: str, org: str, repo: str) -> str:
    s = STRINGS[lang]
    link = (f'<a href="https://github.com/{org}/{repo}/releases/latest" '
            f'rel="noopener">{s["download_fallback_link"]}</a>')
    return s["download_fallback"].format(link=link)


# ---------------------------------------------------------------------------
# Page assembly
# ---------------------------------------------------------------------------
def base_context(lang: str, dir_: str, alt_dir: str, title: str, description: str, content: str,
                 jsonld: str = "") -> dict:
    s = STRINGS[lang]
    return {
        "html_lang": s["html_lang"],
        "title": title,
        "description": description,
        "root": asset_root(dir_),
        "org": ORG,
        "content": content,
        "skip_link": s["skip_link"],
        "brand_name": s["brand_name"],
        "nav_plugins": s["nav_plugins"],
        "nav_guides": s["nav_guides"],
        "guides_href": guides_nav_href(lang, dir_),
        "home_href": home_href(lang, dir_),
        "nav_github": s["nav_github"],
        "lang_switch": lang_switch_nav(lang, dir_, alt_dir),
        "seo_head": seo_head(
            lang, dir_,
            dir_ if lang == "en" else alt_dir,
            alt_dir if lang == "en" else dir_,
            title, description, jsonld,
        ),
        "extra_head": "",
        "footer_note": s["footer_note"],
    }


def write_page(dir_: str, base_tpl: str, ctx: dict) -> None:
    page_dir = DIST / dir_ if dir_ else DIST
    page_dir.mkdir(parents=True, exist_ok=True)
    (page_dir / "index.html").write_text(render(base_tpl, ctx), encoding="utf-8")


def build_index(lang: str, index_tpl: str, base_tpl: str, plugins: list[dict]) -> None:
    s = STRINGS[lang]
    dir_ = lang_dir(lang)
    alt_dir = lang_dir("de" if lang == "en" else "en")
    root = asset_root(dir_)
    cards = "\n".join(build_card(p, lang, root) for p in plugins)
    index_content = render(index_tpl, {
        "site_tagline": s["site_tagline"],
        "hero_sub": s["hero_sub"],
        "emblem_alt": s["emblem_alt"],
        "brand_name": s["brand_name"],
        "cards": cards,
        "root": root,
        "signal_chain_href": rel_link(dir_, lang_dir(lang, "signal-chain")),
        "signal_chain_callout": s["signal_chain_callout"],
        "daws_section": daws_section(lang, root, centered=True),
    })
    jsonld = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Organization",
                "name": SITE_NAME,
                "url": BASE_URL,
                "logo": f"{BASE_URL}assets/favicon-192.png",
                "sameAs": [f"https://github.com/{ORG}"],
            },
            {
                "@type": "WebSite",
                "name": SITE_NAME,
                "url": BASE_URL,
                "inLanguage": ["en", "de"],
            },
        ],
    }, ensure_ascii=False)
    ctx = base_context(lang, dir_, alt_dir, f"{SITE_NAME} — {s['site_tagline']}", s["site_description"], index_content, jsonld=jsonld)
    if lang == "en":
        ctx["extra_head"] = ROOT_REDIRECT_SCRIPT
    write_page(dir_, base_tpl, ctx)


def build_plugin_page(lang: str, plugin_tpl: str, base_tpl: str, plugin: dict, manuals_present: dict, guides_present: dict) -> None:
    s = STRINGS[lang]
    slug = plugin["slug"]
    dir_ = lang_dir(lang, slug)
    alt_dir = lang_dir("de" if lang == "en" else "en", slug)
    root = asset_root(dir_)

    name = plugin["name"]
    role = loc(plugin, lang, "role")
    tagline = loc(plugin, lang, "tagline")
    description = loc(plugin, lang, "description")
    features = loc(plugin, lang, "features")

    note = plugin.get("note")
    note_html = f'<p class="rename-note">{html.escape(note)}</p>' if note else ""
    features_html = "\n".join(feature_item(f) for f in features)

    content = render(plugin_tpl, {
        "slug": slug,
        "name": html.escape(name),
        "repo": plugin["repo"],
        "role": html.escape(role),
        "tagline": html.escape(tagline),
        "description": html.escape(description),
        "note": note_html,
        "features": features_html,
        "org": ORG,
        "root": root,
        "all_plugins": s["all_plugins"],
        "formats_line": s["formats_line"],
        "about_heading": s["about_heading"],
        "features_heading": s["features_heading"],
        "download_heading": s["download_heading"],
        "download_fallback": build_download_fallback(lang, ORG, plugin["repo"]),
        "signing_note": s["signed_note"],
        "daws_section": daws_section(lang, root),
        "lore_section": lore_section(plugin, lang, s),
        "engineering_section": engineering_section(plugin, lang, s),
        "screenshots_section": screenshots_section(plugin, lang, root),
        "audio_section": audio_section(plugin, lang, root),
        "support_heading": s["support_heading"],
        "support_body": s["support_body"],
        "donate_note": s["donate_note"],
        "links_heading": s["links_heading"],
        "link_source": s["link_source"],
        "guide_link_item": guide_link_item(plugin, lang, guides_present),
        "manual_link_item": manual_link_item(plugin, lang, manuals_present),
        "link_releases": s["link_releases"],
        "link_license": s["link_license"],
        "release_notes_label": html.escape(s["release_notes_label"]),
    })
    jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": name,
        "description": description,
        "url": page_url(dir_),
        "image": f"{BASE_URL}assets/icons/{slug}-352.webp",
        "applicationCategory": "MultimediaApplication",
        "applicationSubCategory": "Audio plugin",
        "operatingSystem": "macOS, Windows",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
        "license": "https://www.gnu.org/licenses/agpl-3.0",
        "downloadUrl": f"https://github.com/{ORG}/{plugin['repo']}/releases",
        "author": {"@type": "Organization", "name": SITE_NAME, "url": BASE_URL},
    }, ensure_ascii=False)
    ctx = base_context(lang, dir_, alt_dir, f"{name} — {role} | {SITE_NAME}", tagline, content, jsonld=jsonld)
    write_page(dir_, base_tpl, ctx)


def lore_section(plugin: dict, lang: str, s: dict) -> str:
    lore = loc(plugin, lang, "lore") if plugin.get("lore") else ""
    if not lore:
        return ""
    return (
        '<section class="section" aria-labelledby="lore-heading">\n'
        f'  <h2 id="lore-heading">{s["lore_heading"]}</h2>\n'
        f'  <p class="prose lore">{html.escape(lore)}</p>\n'
        '</section>'
    )


def engineering_section(plugin: dict, lang: str, s: dict) -> str:
    """The 'Under the hood' engineering deep-dive — sourced from the SOTA
    dossiers (see .scaffold/research/2026-07-25-sota/website-dossier-*.md),
    authored per plugin as Markdown (bold-lead paragraphs, occasionally a
    table) and rendered through the same vendored lib_md renderer the manual
    pages use, so it gets identical typography for free. Optional per
    plugin, same English-fallback convention as lore_section above."""
    engineering = loc(plugin, lang, "engineering") if plugin.get("engineering") else ""
    if not engineering:
        return ""
    body_html = lib_md.render(engineering)
    return (
        '<section class="section" aria-labelledby="engineering-heading">\n'
        f'  <h2 id="engineering-heading">{s["engineering_heading"]}</h2>\n'
        f'  <div class="manual engineering-body">\n{body_html}\n  </div>\n'
        '</section>'
    )


def build_manual_page(lang: str, manual_tpl: str, base_tpl: str, plugin: dict, manuals_present: dict) -> None:
    s = STRINGS[lang]
    slug = plugin["slug"]
    path = manual_path(slug, lang)
    if not path.is_file():
        return
    dir_ = lang_dir(lang, slug, "manual")
    plugin_dir = lang_dir(lang, slug)

    has_en = manuals_present.get((slug, "en"), False)
    has_de = manuals_present.get((slug, "de"), False)
    if lang == "en":
        alt_dir = lang_dir("de", slug, "manual") if has_de else lang_dir("de", slug)
    else:
        alt_dir = lang_dir("en", slug, "manual") if has_en else lang_dir("en", slug)

    markdown_text = load_manual_markdown(path)
    rewriter = manual_link_rewriter(ORG, plugin["repo"])
    body_html = lib_md.render(markdown_text, link_rewriter=rewriter)

    name = plugin["name"]
    content = render(manual_tpl, {
        "manual_back": s["manual_back"].format(name=html.escape(name)),
        "manual_content": body_html,
    })
    title = f"{name} — {s['manual_title_suffix']} | {SITE_NAME}"
    description = s["manual_description"].format(name=name, site_name=SITE_NAME)
    ctx = base_context(lang, dir_, alt_dir, title, description, content)
    write_page(dir_, base_tpl, ctx)


def build_guide_page(lang: str, guide_tpl: str, base_tpl: str, plugin: dict, guides_present: dict) -> None:
    """Per-plugin 'How-to guide' — hand-authored Markdown (not repo-synced,
    unlike manuals) under data/guides/<slug>.<lang>.md, rendered through the
    same lib_md renderer and the .manual typography, at /<slug>/guide/."""
    s = STRINGS[lang]
    slug = plugin["slug"]
    path = guide_path(slug, lang)
    if not path.is_file():
        return
    dir_ = lang_dir(lang, slug, "guide")

    has_en = guides_present.get((slug, "en"), False)
    has_de = guides_present.get((slug, "de"), False)
    if lang == "en":
        alt_dir = lang_dir("de", slug, "guide") if has_de else lang_dir("de", slug)
    else:
        alt_dir = lang_dir("en", slug, "guide") if has_en else lang_dir("en", slug)

    markdown_text = path.read_text(encoding="utf-8")
    body_html = lib_md.render(markdown_text)

    name = plugin["name"]
    content = render(guide_tpl, {
        "guide_back_href": "../index.html",
        "guide_back_label": s["manual_back"].format(name=html.escape(name)),
        "guide_content": body_html,
    })
    title = f"{name} — {s['guide_label']} | {SITE_NAME}"
    description = s["guide_description"].format(name=name, site_name=SITE_NAME)
    ctx = base_context(lang, dir_, alt_dir, title, description, content)
    write_page(dir_, base_tpl, ctx)


def build_signal_chain_page(lang: str, guide_tpl: str, base_tpl: str) -> None:
    """The one suite-level guide page — /signal-chain/ + /de/signal-chain/ —
    sits at the same tree depth as a product page, so its breadcrumb reuses
    the "All plugins" back-link the exact same way plugin.html's does."""
    s = STRINGS[lang]
    path = GUIDES_DIR / f"signal-chain.{lang}.md"
    if not path.is_file():
        return
    dir_ = lang_dir(lang, "signal-chain")
    alt_dir = lang_dir("de" if lang == "en" else "en", "signal-chain")

    markdown_text = path.read_text(encoding="utf-8")
    body_html = lib_md.render(markdown_text)

    content = render(guide_tpl, {
        "guide_back_href": "../index.html",
        "guide_back_label": s["all_plugins"],
        "guide_content": body_html,
    })
    title = f"{s['signal_chain_title']} | {SITE_NAME}"
    description = s["signal_chain_description"]
    ctx = base_context(lang, dir_, alt_dir, title, description, content)
    write_page(dir_, base_tpl, ctx)


def build_404(base_tpl: str) -> None:
    """Bilingual 404 page. GitHub Pages serves dist/404.html for any missing
    path, at any depth — so every internal reference on this one page must be
    absolute (root=BASE_URL takes care of the template chrome)."""
    en, de = STRINGS["en"], STRINGS["de"]
    content = f"""<section class="hero">
  <img class="hero-emblem" src="{BASE_URL}assets/org-300.webp" alt="" width="150" height="150">
  <h1 class="hero-title">404</h1>
  <p class="hero-tagline">This page does not exist. <span lang="de">Diese Seite existiert nicht.</span></p>
  <div class="ornament" role="presentation"><span></span></div>
  <p class="hero-sub">The page you were looking for has moved or never existed.<br>
  <span lang="de">Die gesuchte Seite wurde verschoben oder hat nie existiert.</span></p>
  <p class="guides-callout"><a href="{BASE_URL}">{html.escape(en["all_plugins"])}</a>
  &ensp;<span aria-hidden="true">·</span>&ensp;
  <a href="{BASE_URL}de/" lang="de">{html.escape(de["all_plugins"])}</a></p>
</section>"""
    ctx = {
        "html_lang": "en",
        "title": f"404 — {SITE_NAME}",
        "description": "Page not found.",
        "root": BASE_URL,
        "org": ORG,
        "content": content,
        "skip_link": en["skip_link"],
        "brand_name": en["brand_name"],
        "nav_plugins": en["nav_plugins"],
        "nav_guides": en["nav_guides"],
        "guides_href": f"{BASE_URL}signal-chain/",
        "home_href": BASE_URL,
        "nav_github": en["nav_github"],
        "lang_switch": "",
        "seo_head": '<meta name="robots" content="noindex">',
        "extra_head": "",
        "footer_note": en["footer_note"],
    }
    (DIST / "404.html").write_text(render(base_tpl, ctx), encoding="utf-8")


def write_sitemap_and_robots() -> None:
    """sitemap.xml with bilingual xhtml:link alternates + robots.txt.

    English URLs carry their German twin as an alternate (and vice versa is
    implied); a German-only page (possible in theory, never in practice)
    would still get its own <url> entry.
    """
    dirs = sorted(
        "" if (rel := str(p.parent.relative_to(DIST))) == "." else rel
        for p in DIST.rglob("index.html")
    )
    dir_set = set(dirs)
    entries = []
    for d in dirs:
        is_de = d == "de" or d.startswith("de/")
        if is_de:
            en_twin = d[3:] if d.startswith("de/") else ""
            if en_twin in dir_set:
                continue  # listed as alternate of its English twin
            entries.append(f"  <url>\n    <loc>{page_url(d)}</loc>\n  </url>")
            continue
        de_twin = f"de/{d}" if d else "de"
        alt = ""
        if de_twin in dir_set:
            alt = (
                f'\n    <xhtml:link rel="alternate" hreflang="en" href="{page_url(d)}"/>'
                f'\n    <xhtml:link rel="alternate" hreflang="de" href="{page_url(de_twin)}"/>'
                f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{page_url(d)}"/>'
            )
        entries.append(f"  <url>\n    <loc>{page_url(d)}</loc>{alt}\n  </url>")
    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(entries)
        + "\n</urlset>\n"
    )
    (DIST / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    (DIST / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}sitemap.xml\n", encoding="utf-8"
    )


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------
def build_site() -> tuple[list[str], list[str], int]:
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

    # Assets (icons, emblem, css, js, and any per-plugin media directories)
    # are shared by both language trees — copied once at dist/assets/.
    shutil.copytree(ROOT / "assets", DIST / "assets")

    base = read_template("base.html")
    index_tpl = read_template("index.html")
    plugin_tpl = read_template("plugin.html")
    manual_tpl = read_template("manual.html")
    guide_tpl = read_template("guide.html")

    manuals_present: dict[tuple[str, str], bool] = {}
    manuals_synced: list[str] = []
    manuals_missing: list[str] = []
    for plugin in plugins:
        slug = plugin["slug"]
        has_en = manual_path(slug, "en").is_file()
        has_de = manual_path(slug, "de").is_file()
        manuals_present[(slug, "en")] = has_en
        manuals_present[(slug, "de")] = has_de
        if has_en:
            manuals_synced.append(slug)
        else:
            manuals_missing.append(slug)

    guides_present: dict[tuple[str, str], bool] = {}
    for plugin in plugins:
        slug = plugin["slug"]
        guides_present[(slug, "en")] = guide_path(slug, "en").is_file()
        guides_present[(slug, "de")] = guide_path(slug, "de").is_file()

    page_count = 0
    for lang in LANGS:
        build_index(lang, index_tpl, base, plugins)
        page_count += 1
        build_signal_chain_page(lang, guide_tpl, base)
        if (GUIDES_DIR / f"signal-chain.{lang}.md").is_file():
            page_count += 1
        for plugin in plugins:
            build_plugin_page(lang, plugin_tpl, base, plugin, manuals_present, guides_present)
            page_count += 1
            manual_path_for_lang = manual_path(plugin["slug"], lang)
            if manual_path_for_lang.is_file():
                build_manual_page(lang, manual_tpl, base, plugin, manuals_present)
                page_count += 1
            if guide_path(plugin["slug"], lang).is_file():
                build_guide_page(lang, guide_tpl, base, plugin, guides_present)
                page_count += 1

    build_404(base)
    page_count += 1
    write_sitemap_and_robots()

    print(f"built {page_count} pages -> {DIST}")
    return manuals_synced, manuals_missing, page_count


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
    synced, missing, count = build_site()
    check_links()
    print(f"manuals synced (en): {synced}")
    if missing:
        print(f"manuals missing (no page rendered): {missing}")
