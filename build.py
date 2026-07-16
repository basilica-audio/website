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

LANGS = ("en", "de")

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
AUDIO_EXTS = {".mp3", ".wav", ".ogg", ".flac", ".m4a"}
AUDIO_MIME = {
    ".mp3": "audio/mpeg", ".wav": "audio/wav", ".ogg": "audio/ogg",
    ".flac": "audio/flac", ".m4a": "audio/mp4",
}

PLACEHOLDER_RE = re.compile(r"\{\{[a-z_]+\}\}")

MANUALS_DIR = ROOT / "data" / "manuals"

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
        "signed_note": ("The macOS binaries are Developer-ID-signed, notarized by Apple "
                        "and stapled — they install and open without Gatekeeper warnings. "
                        "Windows builds are not yet Authenticode-signed; SmartScreen may "
                        "warn about an unknown publisher."),
        "features_heading": "Features",
        "download_heading": "Download",
        "download_fallback": "The latest builds are published on {link}.",
        "download_fallback_link": "GitHub&nbsp;Releases",
        "unsigned_title": "A note on unsigned binaries.",
        "unsigned_body": ("These builds are not yet code-signed — the signing and "
                           "notarization pipeline is still in progress. Your operating "
                           "system will warn you on first launch:"),
        "unsigned_macos": ("<strong>macOS</strong> — Gatekeeper will block the first open. "
                            "Right-click the plugin or app and choose <em>Open</em>, or "
                            "remove the quarantine flag in Terminal: "
                            "<code>xattr&nbsp;-dr&nbsp;com.apple.quarantine&nbsp;&lt;file&gt;</code>."),
        "unsigned_windows": ("<strong>Windows</strong> — SmartScreen may show “Windows "
                              "protected your PC”. Choose <em>More info</em> → "
                              "<em>Run anyway</em>."),
        "unsigned_footer": ("Only ever do this for builds downloaded directly from this "
                             "project’s GitHub releases."),
        "screenshots_heading": "Screenshots",
        "screenshots_empty": "Coming with the next release.",
        "screenshots_empty_sub": ("The custom interface is currently in design — "
                                   "screenshots will appear here as soon as it ships."),
        "audio_heading": "Audio examples",
        "audio_empty": "Coming with the next release.",
        "audio_empty_sub": ("Before/after clips are being recorded — audio examples will "
                             "appear here with an upcoming release."),
        "audio_download_prefix": "Download {caption}",
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
                         "macOS binaries are Developer-ID-signed and notarized."),
        "manual_back": "Back to {name}",
        "manual_title_suffix": "User manual",
        "manual_description": "User manual for {name} — {site_name}.",
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
        "signed_note": ("Die macOS-Binaries sind Developer-ID-signiert, von Apple "
                        "notarisiert und gestapelt — sie installieren und öffnen ohne "
                        "Gatekeeper-Warnung. Windows-Builds sind noch nicht "
                        "Authenticode-signiert; SmartScreen warnt eventuell vor einem "
                        "unbekannten Herausgeber."),
        "features_heading": "Funktionen",
        "download_heading": "Download",
        "download_fallback": "Die aktuellen Builds werden auf {link} veröffentlicht.",
        "download_fallback_link": "GitHub&nbsp;Releases",
        "unsigned_title": "Hinweis zu unsignierten Binaries.",
        "unsigned_body": ("Diese Builds sind noch nicht code-signiert — die Signierungs- "
                           "und Notarisierungs-Pipeline ist noch in Arbeit. Dein "
                           "Betriebssystem warnt dich beim ersten Start:"),
        "unsigned_macos": ("<strong>macOS</strong> — Gatekeeper blockiert das erste "
                            "Öffnen. Rechtsklick auf das Plugin bzw. die App und "
                            "<em>Öffnen</em> wählen, oder das Quarantäne-Flag im "
                            "Terminal entfernen: "
                            "<code>xattr&nbsp;-dr&nbsp;com.apple.quarantine&nbsp;&lt;Datei&gt;</code>."),
        "unsigned_windows": ("<strong>Windows</strong> — SmartScreen zeigt eventuell "
                              "„Der Computer wurde durch Windows geschützt“. "
                              "<em>Weitere Informationen</em> → "
                              "<em>Trotzdem ausführen</em> wählen."),
        "unsigned_footer": ("Mach das ausschließlich bei Builds, die direkt aus den "
                             "GitHub-Releases dieses Projekts stammen."),
        "screenshots_heading": "Screenshots",
        "screenshots_empty": "Kommt mit dem nächsten Release.",
        "screenshots_empty_sub": ("Die individuelle Oberfläche befindet sich aktuell in "
                                   "der Gestaltung — Screenshots erscheinen hier, sobald "
                                   "sie fertig ist."),
        "audio_heading": "Hörbeispiele",
        "audio_empty": "Kommt mit dem nächsten Release.",
        "audio_empty_sub": ("Vorher/Nachher-Clips werden gerade aufgenommen — "
                             "Hörbeispiele erscheinen hier mit einem kommenden Release."),
        "audio_download_prefix": "{caption} herunterladen",
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


def hreflang_tags(this_dir: str, en_dir: str, de_dir: str) -> str:
    en_href = rel_link(this_dir, en_dir)
    de_href = rel_link(this_dir, de_dir)
    return (
        f'<link rel="alternate" hreflang="en" href="{en_href}">\n'
        f'<link rel="alternate" hreflang="de" href="{de_href}">\n'
        f'<link rel="alternate" hreflang="x-default" href="{en_href}">'
    )


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


def screenshots_section(plugin: dict, lang: str, root: str) -> str:
    s = STRINGS[lang]
    shots = collect_media(plugin, IMAGE_EXTS, "screenshots")
    if not shots:
        return f"""<section class="section" aria-labelledby="screenshots-heading">
  <h2 id="screenshots-heading">{s['screenshots_heading']}</h2>
  <div class="empty-state">
    <span class="empty-glyph" aria-hidden="true">&#9672;</span>
    <p>{s['screenshots_empty']}</p>
    <p class="empty-sub">{s['screenshots_empty_sub']}</p>
  </div>
</section>"""
    figures = "\n".join(
        f"""    <figure>
      <img src="{root}assets/{plugin['slug']}/{html.escape(name)}" alt="{html.escape(caption)}" loading="lazy">
      <figcaption>{html.escape(caption)}</figcaption>
    </figure>"""
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


def build_card(plugin: dict, lang: str, root: str) -> str:
    s = STRINGS[lang]
    slug, name = plugin["slug"], plugin["name"]
    role = loc(plugin, lang, "role")
    return f"""  <article class="card">
    <img class="card-icon" src="{root}assets/icons/{slug}.png" alt="" width="92" height="92">
    <h2><a class="card-link" href="{slug}/index.html">{html.escape(name)}</a></h2>
    <p class="card-role">{html.escape(role)}</p>
    <p class="card-actions">
      <span class="details-hint" aria-hidden="true">{s['details_hint']}&nbsp;&rarr;</span>
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


def build_download_fallback(lang: str, org: str, repo: str) -> str:
    s = STRINGS[lang]
    link = (f'<a href="https://github.com/{org}/{repo}/releases/latest" '
            f'rel="noopener">{s["download_fallback_link"]}</a>')
    return s["download_fallback"].format(link=link)


# ---------------------------------------------------------------------------
# Page assembly
# ---------------------------------------------------------------------------
def base_context(lang: str, dir_: str, alt_dir: str, title: str, description: str, content: str) -> dict:
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
        "nav_github": s["nav_github"],
        "lang_switch": lang_switch_nav(lang, dir_, alt_dir),
        "hreflang_tags": hreflang_tags(dir_, dir_ if lang == "en" else alt_dir, alt_dir if lang == "en" else dir_),
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
    })
    ctx = base_context(lang, dir_, alt_dir, f"{SITE_NAME} — {s['site_tagline']}", s["site_description"], index_content)
    if lang == "en":
        ctx["extra_head"] = ROOT_REDIRECT_SCRIPT
    write_page(dir_, base_tpl, ctx)


def build_plugin_page(lang: str, plugin_tpl: str, base_tpl: str, plugin: dict, manuals_present: dict) -> None:
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
        "lore_section": lore_section(plugin, lang, s),
        "screenshots_section": screenshots_section(plugin, lang, root),
        "audio_section": audio_section(plugin, lang, root),
        "support_heading": s["support_heading"],
        "support_body": s["support_body"],
        "donate_note": s["donate_note"],
        "links_heading": s["links_heading"],
        "link_source": s["link_source"],
        "manual_link_item": manual_link_item(plugin, lang, manuals_present),
        "link_releases": s["link_releases"],
        "link_license": s["link_license"],
        "release_notes_label": html.escape(s["release_notes_label"]),
    })
    ctx = base_context(lang, dir_, alt_dir, f"{name} — {role} | {SITE_NAME}", tagline, content)
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

    page_count = 0
    for lang in LANGS:
        build_index(lang, index_tpl, base, plugins)
        page_count += 1
        for plugin in plugins:
            build_plugin_page(lang, plugin_tpl, base, plugin, manuals_present)
            page_count += 1
            manual_path_for_lang = manual_path(plugin["slug"], lang)
            if manual_path_for_lang.is_file():
                build_manual_page(lang, manual_tpl, base, plugin, manuals_present)
                page_count += 1

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
