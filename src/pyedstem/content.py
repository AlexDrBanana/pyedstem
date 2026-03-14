"""Helpers for converting content into Ed-compatible formats."""

from __future__ import annotations

import html
import re

from markdownify import markdownify as html_to_markdown_converter

_FENCED_CODE_BLOCK_RE = re.compile(
    r"```(?P<language>[^\n`]*)\n(?P<code>.*?)```",
    re.DOTALL,
)


def markdown_to_ed_document(markdown: str) -> str:
    """Convert markdown into the Ed XML document format used by comments.

    The converter currently preserves plain paragraphs and fenced code blocks.
    Non-code text is split into paragraph elements, while fenced blocks are
    emitted as Ed ``codeblock`` elements.

    Args:
        markdown: Markdown source to convert.

    Returns:
        A string containing an Ed ``<document version="2.0">`` payload.
        Blank input produces a minimal empty paragraph document.
    """
    stripped = markdown.strip()
    if not stripped:
        return '<document version="2.0"><paragraph></paragraph></document>'

    blocks: list[str] = []
    remaining = stripped

    while remaining:
        code_match = _FENCED_CODE_BLOCK_RE.search(remaining)
        if code_match is None:
            blocks.extend(_paragraph_blocks(remaining))
            break

        before = remaining[: code_match.start()].strip()
        if before:
            blocks.extend(_paragraph_blocks(before))

        language = code_match.group("language").strip()
        code = html.escape(code_match.group("code").rstrip("\n"))
        if language:
            blocks.append(
                f'<codeblock language="{html.escape(language)}">{code}</codeblock>'
            )
        else:
            blocks.append(f"<codeblock>{code}</codeblock>")

        remaining = remaining[code_match.end() :].strip()

    return f'<document version="2.0">{"".join(blocks)}</document>'


def html_to_markdown(content: str) -> str:
    """Convert Ed HTML content into markdown.

    This is mainly useful when exporting or staging existing Ed thread content
    for local review and editing.

    Args:
        content: HTML content returned by Ed.

    Returns:
        A markdown representation of the HTML content with ATX headings.
    """
    return html_to_markdown_converter(content or "", heading_style="ATX").strip()


def _paragraph_blocks(text: str) -> list[str]:
    """Convert free-form markdown text into Ed XML paragraph blocks.

    Args:
        text: Markdown text without fenced code blocks.

    Returns:
        A list of serialized Ed ``<paragraph>`` elements.
    """
    paragraphs = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]
    xml_paragraphs: list[str] = []

    for paragraph in paragraphs:
        escaped = html.escape(paragraph).replace("\n", "<br>")
        xml_paragraphs.append(f"<paragraph>{escaped}</paragraph>")

    return xml_paragraphs
