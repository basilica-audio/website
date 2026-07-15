"""lib_md — a small, dependency-free Markdown-to-HTML renderer.

Python standard library only (html, re). Written for the Basilica Audio
website's user-manual pages: it covers exactly the subset of Markdown those
manuals use, deliberately and nothing more.

Supported:
  - ATX headings (# through ######), each gets a GitHub-style `id` slug so
    in-document "#anchor" links (used throughout the manuals) work.
  - Paragraphs, with inline **bold**, *italic*, `inline code`, and
    [text](url) links.
  - Fenced code blocks (```lang ... ```), rendered verbatim/escaped.
  - Unordered lists (-, *, +) and ordered lists (1.), including lazily
    wrapped continuation lines (no blank line, no new marker).
  - GitHub-style pipe tables, including alignment colons.
  - Blockquotes (consecutive `>` lines).
  - Horizontal rules (---, ***, ___ on their own line).

Explicitly NOT supported: nested lists, raw HTML passthrough, footnotes,
task-list checkboxes, definition lists. Raw HTML in the source is escaped
(shown as literal text) rather than executed — this renderer never emits an
HTML tag that wasn't produced by one of the constructs above, which keeps it
simple and safe against whatever ends up in a manual someday.

Public API: render(markdown_text: str, *, link_rewriter=None) -> str
"""
from __future__ import annotations

import html
import re
from typing import Callable, List, Optional, Tuple

LinkRewriter = Callable[[str], str]

_ATX_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
_HR_RE = re.compile(r"^ {0,3}((-[ \t]*){3,}|(\*[ \t]*){3,}|(_[ \t]*){3,})$")
_FENCE_RE = re.compile(r"^ {0,3}```[ \t]*([\w+-]*)[ \t]*$")
_UL_RE = re.compile(r"^ {0,3}[-*+]\s+(.*)$")
_OL_RE = re.compile(r"^ {0,3}(\d+)\.\s+(.*)$")
_BQ_RE = re.compile(r"^ {0,3}>\s?(.*)$")
_TABLE_SEP_RE = re.compile(r"^\s*\|?\s*:?-{1,}:?\s*(\|\s*:?-{1,}:?\s*)+\|?\s*$")

_CODE_SPAN_RE = re.compile(r"`([^`]+)`")
_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
_BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
_ITALIC_RE = re.compile(r"\*(.+?)\*")

_SLUG_STRIP_RE = re.compile(r"[^\w\s-]")
_SLUG_WS_RE = re.compile(r"[\s_]+")
_SLUG_DASH_RE = re.compile(r"-{2,}")


def _slugify(text: str) -> str:
    s = text.strip().lower()
    s = _SLUG_STRIP_RE.sub("", s)
    s = _SLUG_WS_RE.sub("-", s)
    s = _SLUG_DASH_RE.sub("-", s)
    return s.strip("-")


class _SlugRegistry:
    def __init__(self) -> None:
        self._seen: dict[str, int] = {}

    def make(self, text: str) -> str:
        base = _slugify(text) or "section"
        count = self._seen.get(base, 0)
        self._seen[base] = count + 1
        return base if count == 0 else f"{base}-{count}"


def _inline(text: str, link_rewriter: Optional[LinkRewriter]) -> str:
    """Render inline markdown within a single logical span of text."""
    # 1. Pull out code spans first so their contents are immune to every
    #    other inline rule (bold/italic markers, link brackets, HTML escape
    #    handled separately below for the code content itself).
    code_spans: List[str] = []

    def _stash_code(m: re.Match) -> str:
        code_spans.append(m.group(1))
        return f"\x00CODE{len(code_spans) - 1}\x00"

    text = _CODE_SPAN_RE.sub(_stash_code, text)

    # 2. Escape everything else as literal text — this is what keeps any
    #    raw HTML in the source inert (shown as text, never executed).
    text = html.escape(text, quote=True)

    # 3. Links — operate before bold/italic so an emphasis marker adjacent
    #    to a link's brackets doesn't get misparsed.
    def _link(m: re.Match) -> str:
        label, url = m.group(1), m.group(2)
        if link_rewriter is not None:
            url = link_rewriter(html.unescape(url))
            url = html.escape(url, quote=True)
        return f'<a href="{url}">{label}</a>'

    text = _LINK_RE.sub(_link, text)

    # 4. Bold, then italic (order matters: consumes ** before single *).
    text = _BOLD_RE.sub(r"<strong>\1</strong>", text)
    text = _ITALIC_RE.sub(r"<em>\1</em>", text)

    # 5. Restore code spans as <code>, HTML-escaping their raw content.
    def _restore_code(m: re.Match) -> str:
        idx = int(m.group(1))
        return f"<code>{html.escape(code_spans[idx], quote=True)}</code>"

    text = re.sub(r"\x00CODE(\d+)\x00", _restore_code, text)
    return text


def _render_table(rows: List[str], link_rewriter: Optional[LinkRewriter]) -> str:
    def split_row(row: str) -> List[str]:
        r = row.strip()
        if r.startswith("|"):
            r = r[1:]
        if r.endswith("|"):
            r = r[:-1]
        # Split on unescaped pipes.
        cells = re.split(r"(?<!\\)\|", r)
        return [c.strip().replace(r"\|", "|") for c in cells]

    header_cells = split_row(rows[0])
    align_cells = split_row(rows[1])
    aligns: List[Optional[str]] = []
    for a in align_cells:
        left = a.startswith(":")
        right = a.endswith(":")
        if left and right:
            aligns.append("center")
        elif right:
            aligns.append("right")
        elif left:
            aligns.append("left")
        else:
            aligns.append(None)

    def style_for(i: int) -> str:
        if i < len(aligns) and aligns[i]:
            return f' style="text-align:{aligns[i]}"'
        return ""

    out = ['<div class="table-scroll"><table>', "<thead><tr>"]
    for i, cell in enumerate(header_cells):
        out.append(f"<th{style_for(i)}>{_inline(cell, link_rewriter)}</th>")
    out.append("</tr></thead><tbody>")
    for row in rows[2:]:
        cells = split_row(row)
        out.append("<tr>")
        for i, cell in enumerate(cells):
            out.append(f"<td{style_for(i)}>{_inline(cell, link_rewriter)}</td>")
        out.append("</tr>")
    out.append("</tbody></table></div>")
    return "\n".join(out)


def render(markdown_text: str, *, link_rewriter: Optional[LinkRewriter] = None) -> str:
    """Render a Markdown document to an HTML fragment (no <html>/<body>)."""
    lines = markdown_text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    n = len(lines)
    i = 0
    out: List[str] = []
    slugs = _SlugRegistry()

    def is_blank(line: str) -> bool:
        return line.strip() == ""

    while i < n:
        line = lines[i]

        if is_blank(line):
            i += 1
            continue

        # Fenced code block.
        fence_m = _FENCE_RE.match(line)
        if fence_m:
            lang = fence_m.group(1)
            i += 1
            code_lines: List[str] = []
            while i < n and not _FENCE_RE.match(lines[i]):
                code_lines.append(lines[i])
                i += 1
            i += 1  # consume closing fence (or EOF)
            code = html.escape("\n".join(code_lines), quote=True)
            cls = f' class="language-{html.escape(lang)}"' if lang else ""
            out.append(f"<pre><code{cls}>{code}</code></pre>")
            continue

        # Horizontal rule.
        if _HR_RE.match(line):
            out.append("<hr>")
            i += 1
            continue

        # ATX heading.
        atx_m = _ATX_RE.match(line)
        if atx_m:
            level = len(atx_m.group(1))
            text = atx_m.group(2)
            slug = slugs.make(text)
            out.append(f'<h{level} id="{slug}">{_inline(text, link_rewriter)}</h{level}>')
            i += 1
            continue

        # Table: current line + next line looks like a separator row.
        if "|" in line and i + 1 < n and _TABLE_SEP_RE.match(lines[i + 1]):
            table_rows = [line, lines[i + 1]]
            i += 2
            while i < n and not is_blank(lines[i]) and "|" in lines[i]:
                table_rows.append(lines[i])
                i += 1
            out.append(_render_table(table_rows, link_rewriter))
            continue

        # Blockquote.
        if _BQ_RE.match(line):
            bq_lines: List[str] = []
            while i < n and _BQ_RE.match(lines[i]):
                bq_lines.append(_BQ_RE.match(lines[i]).group(1))
                i += 1
            # Split accumulated lines into paragraphs on blank entries.
            paras: List[List[str]] = [[]]
            for bl in bq_lines:
                if bl.strip() == "":
                    paras.append([])
                else:
                    paras[-1].append(bl)
            rendered = "".join(
                f"<p>{_inline(' '.join(p), link_rewriter)}</p>"
                for p in paras
                if p
            )
            out.append(f"<blockquote>{rendered}</blockquote>")
            continue

        # Lists (unordered / ordered), with lazy continuation lines.
        ul_m = _UL_RE.match(line)
        ol_m = _OL_RE.match(line)
        if ul_m or ol_m:
            ordered = ol_m is not None
            items: List[str] = [ (ol_m.group(2) if ol_m else ul_m.group(1)) ]
            i += 1
            while i < n:
                nxt = lines[i]
                if is_blank(nxt):
                    break
                nxt_ul = _UL_RE.match(nxt)
                nxt_ol = _OL_RE.match(nxt)
                if ordered and nxt_ol:
                    items.append(nxt_ol.group(2))
                    i += 1
                elif (not ordered) and nxt_ul:
                    items.append(nxt_ul.group(1))
                    i += 1
                elif nxt_ul or nxt_ol:
                    # Marker type switched — end this list, let the outer
                    # loop start a new one.
                    break
                elif (
                    _ATX_RE.match(nxt)
                    or _FENCE_RE.match(nxt)
                    or _HR_RE.match(nxt)
                    or _BQ_RE.match(nxt)
                    or ("|" in nxt and i + 1 < n and _TABLE_SEP_RE.match(lines[i + 1] if i + 1 < n else ""))
                ):
                    break
                else:
                    # Lazy continuation of the current item.
                    items[-1] = items[-1] + " " + nxt.strip()
                    i += 1
            tag = "ol" if ordered else "ul"
            rendered_items = "\n".join(
                f"  <li>{_inline(it, link_rewriter)}</li>" for it in items
            )
            out.append(f"<{tag}>\n{rendered_items}\n</{tag}>")
            continue

        # Paragraph: collect until a blank line or a line starting a new
        # block construct.
        para_lines = [line]
        i += 1
        while i < n and not is_blank(lines[i]) and not (
            _ATX_RE.match(lines[i])
            or _FENCE_RE.match(lines[i])
            or _HR_RE.match(lines[i])
            or _UL_RE.match(lines[i])
            or _OL_RE.match(lines[i])
            or _BQ_RE.match(lines[i])
            or ("|" in lines[i] and i + 1 < n and _TABLE_SEP_RE.match(lines[i + 1]))
        ):
            para_lines.append(lines[i])
            i += 1
        out.append(f"<p>{_inline(' '.join(l.strip() for l in para_lines), link_rewriter)}</p>")

    return "\n".join(out)
