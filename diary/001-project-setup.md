# 001 — Project Setup

**Date**: 2026-04-24
**Tool**: GitHub Copilot
**Model**: Claude Haiku 4.5
**Iterations**: 1

## Prompt

**2026-04-24 00:00**

Create a python 3.12 project called sign-pdf using uv (from Astral) for dependency management. The project should separate parsing of the SVG file with the signature (`parse_svg.py`), redrawing of the path from the SVG file on a given PDF file (`render_signature.py`) and the cli interface (`cli.py`).

Set up pytest for testing with corresponding test files for each module. Manage all dependencies through pyproject.toml — I'll need pymupdf, click and pytest.

Include a README.md with a brief project description.

Create a diary/ folder for tracking AI interactions. For every prompt cycle in this project, save the interaction record to this folder as a numbered markdown file. Use this format:

    # NNN — Short Title

    **Date**: YYYY-MM-DD
    **Tool**: [tool name]
    **Model**: [model name]
    **Iterations**: [number]

    ## Prompt

    **YYYY-MM-DD HH:MM**

    [The full prompt text as given by the user.]

    If there were follow-up prompts (corrections, clarifications),
    add each as a separate entry with its own timestamp under the
    same Prompt section.

Save this initial setup prompt as diary/001-project-setup.md.

Do NOT implement any logic yet — just create the project structure, configuration, and empty module files with docstrings describing their purpose.

Initialize a git repository and create an initial commit with this scaffolding.

## Summary

Initial project scaffolding created with:
- Python 3.12 project structure
- uv-based dependency management via pyproject.toml
- Three core modules: parse_svg.py, render_signature.py, cli.py
- Pytest test suite with test files for each module
- Dependencies: pymupdf, click, pytest
- README.md with project documentation
- diary/ folder for tracking interactions
- .gitignore for Python/IDE files
- Git repository initialization with first commit
