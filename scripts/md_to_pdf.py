#!/usr/bin/env python3
"""Convert markdown papers to styled PDFs with proper table rendering."""

import sys
import markdown
from weasyprint import HTML

CSS = """
@page {
    size: A4;
    margin: 2.5cm 2cm;
    @bottom-center {
        content: counter(page);
        font-family: 'Georgia', serif;
        font-size: 10pt;
        color: #666;
    }
}

body {
    font-family: 'Georgia', 'Times New Roman', serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #1a1a1a;
    max-width: 100%;
}

h1 {
    font-size: 22pt;
    margin-top: 0;
    margin-bottom: 4pt;
    color: #111;
    page-break-after: avoid;
}

h2 {
    font-size: 16pt;
    margin-top: 28pt;
    margin-bottom: 8pt;
    color: #222;
    border-bottom: 1px solid #ccc;
    padding-bottom: 4pt;
    page-break-after: avoid;
}

h3 {
    font-size: 13pt;
    margin-top: 20pt;
    margin-bottom: 6pt;
    color: #333;
    page-break-after: avoid;
}

p {
    margin: 0 0 8pt 0;
    text-align: justify;
}

strong {
    color: #111;
}

em {
    font-style: italic;
}

hr {
    border: none;
    border-top: 1px solid #ddd;
    margin: 20pt 0;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 12pt 0;
    font-size: 9.5pt;
    page-break-inside: avoid;
}

thead {
    background-color: #f5f5f5;
}

th {
    border: 1px solid #999;
    padding: 6pt 8pt;
    text-align: left;
    font-weight: bold;
    font-size: 9.5pt;
}

td {
    border: 1px solid #ccc;
    padding: 5pt 8pt;
    text-align: left;
    font-size: 9.5pt;
}

tr:nth-child(even) {
    background-color: #fafafa;
}

ul, ol {
    margin: 4pt 0 8pt 0;
    padding-left: 20pt;
}

li {
    margin-bottom: 4pt;
}

code {
    font-family: 'Courier New', monospace;
    font-size: 9pt;
    background-color: #f4f4f4;
    padding: 1pt 3pt;
    border-radius: 2pt;
}

pre {
    font-family: 'Courier New', monospace;
    font-size: 8.5pt;
    background-color: #f4f4f4;
    padding: 10pt;
    border: 1px solid #ddd;
    border-radius: 3pt;
    overflow-x: auto;
    white-space: pre-wrap;
    word-wrap: break-word;
    page-break-inside: avoid;
}

blockquote {
    border-left: 3pt solid #ccc;
    margin: 8pt 0;
    padding: 4pt 12pt;
    color: #555;
}
"""


def convert(md_path, pdf_path):
    with open(md_path, 'r') as f:
        md_text = f.read()

    html_body = markdown.markdown(
        md_text,
        extensions=['tables', 'fenced_code', 'codehilite', 'smarty'],
        extension_configs={'smarty': {'smart_angled_quotes': True}},
    )

    full_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>{CSS}</style>
</head>
<body>
{html_body}
</body>
</html>"""

    HTML(string=full_html).write_pdf(pdf_path)
    print(f"  {pdf_path}")


if __name__ == '__main__':
    papers = [
        ('docs/PAPER_17.md', 'docs/PAPER_17.pdf'),
        ('docs/PAPER_18.md', 'docs/PAPER_18.pdf'),
        ('docs/PAPER_19.md', 'docs/PAPER_19.pdf'),
    ]
    for md, pdf in papers:
        convert(md, pdf)
    print("Done.")
