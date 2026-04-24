# sign-pdf

A tool to sign PDF documents with SVG signatures.

## Overview

`sign-pdf` is a Python utility that enables you to programmatically sign PDF documents by rendering SVG signatures onto them. It provides both a Python API and a command-line interface for integration into your workflows.

## Features

- Parse SVG signature files
- Render signatures onto PDF documents
- Command-line interface for batch processing
- Configurable placement and styling

## Installation

```bash
uv pip install -e .
```

## Usage

### Command Line

```bash
sign-pdf document.pdf signature.svg --page 0 --x 100 --y 100 --output signed.pdf
```

### Python API

```python
from sign_pdf.parse_svg import parse_svg
from sign_pdf.render_signature import render_signature_on_pdf

# Parse the SVG signature
svg_data = parse_svg('signature.svg')

# Render it onto a PDF
render_signature_on_pdf('document.pdf', svg_data, page_number=0, x=100, y=100)
```

## Development

Install development dependencies:

```bash
uv pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

## License

MIT
