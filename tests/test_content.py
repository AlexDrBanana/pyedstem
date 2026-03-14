"""Tests for Ed content conversion helpers."""

from __future__ import annotations

from pyedstem.content import markdown_to_ed_document


def test_markdown_to_ed_document_wraps_content_in_ed_xml() -> None:
    """Posted answers should use the Ed XML document format, not plain HTML."""
    document = markdown_to_ed_document("Hi there\n\nThanks,\nSam")

    assert document.startswith('<document version="2.0">')
    assert "<paragraph>Hi there</paragraph>" in document
    assert document.endswith("</document>")
