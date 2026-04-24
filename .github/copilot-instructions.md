# Sign-PDF -- Project Context for Github Copilot

Reference implementation for the "Sign-PDF" tool.
Demonstrates a professional and secure software development live cycle with TDD, diary entries and clean git history.

## Tech Stack

- Python 3.12, managed with [uv](https://docs.astral.sh/uv/)
- Always use type annotations
- Always write google-style docstrings for modules, classes and functions.
- pymupdf (read, draw, annotate, write PDF files), click (command line interface creation kit)
- pytest with unittest.mock for testing

## Commands

```bash
uv sync                              # Install dependencies
uv run python -m sign_pdf.cli -c <config_file> --in <PDF_to_sign> --out <signed_PDF>        # Run the cli to sign PDFs
uv run pytest -v                     # Run all tests
```

## Config file structure

The configuration file is a json file with the following keys:

- `svg` -- path to the SVG file with the signature.
- `page` -- the page number in the PDF where the signature should be placed (first page is 1).
- `xy` -- a list with the x and y offset in the page to place the signature. (0, 0) is the upper left corner of the pdf and the xy coordinates denote the lower left corner of the signature.
- `width` -- the width of the signature in the PDF
- `height` -- the hight of the signature in the PDF
- `preserve_aspect_ratio` -- should the aspect ratio of the signature in the SVG be preserved when drawn in the PDF

## SVG structure

The signature SVG file contains a path with id `signature` and one path with id `helpline`.

## Architecture

Structure in `src/sign_pdf/`:

- **`cli.py`** - Entry point. Orchestrates: reading config file, parse SVG, render signature on the PDF and save signed PDF.
- **`parse_svg.py`** - Parser for the SVG file.
- **`render_signature.py`** - Redraws the path with the id `signature` on the pdf. Optional you can also redraw the `helpline` and a bounding box around the signature.

## Testing

Tests in `tests/` mirror source structure (`test_parse_svg.py`, `test_render_signature.py`). Tests verify data types, and behavior.
Always use a TDD approach.

## Example files

The directory `example-files/` contains files that may be used during testing as input files. IMPORTANT: Do not change this files in any form!

- **`LoremIpsumFormular.pdf`** - Sample PDF file with a place for a signature.
- **`LoremIpsumFormular.odt`** - Source file for the PDF file.
- **`Signature.png`** - A scan of a hand drawn signature.
- **`signature.svg`** - vectorization of the hand drawn signature. It contains a path with the id `signature` that contains the signature and a path with the id `helpline`.

## Diary

The `diary/` folder contains numbered entries (one per development step), documenting each AI interaction. Entries correspond 1:1 with commits in the git history.

### Diary Entry Format

Each diary entry follows this structure:

```markdown
# NNN — Short Title

**Date**: YYYY-MM-DD
**Tool**: Claude Code / GitHub Copilot / etc.
**Model**: Model name and version
**Iterations**: Number of prompts needed

## Prompt

**YYYY-MM-DD HH:MM**

The exact prompt or instruction given to the AI.

(If multiple iterations were needed, add each follow-up prompt
with its own timestamp.)
```

### Diary Workflow

- **One entry per AI interaction**, committed together with the code changes
- **File naming**: `NNN-short-description.md` (e.g., `003-parse-svg-tests.md`, `004-parse-svg-impl.md`)
- **Commit prefix**: `[diary]` for commits that include diary entries
- When asked to "write a diary entry", create it in `diary/` following this format — reference this section for the structure rather than asking the user to spell it out each time
