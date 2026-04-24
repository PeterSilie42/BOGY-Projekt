"""Command-line interface for signing PDF documents with SVG signatures.

This module provides the CLI entry point for the sign-pdf application,
allowing users to sign PDF documents from the command line.
"""

import click


@click.command()
@click.argument('pdf_path', type=click.Path(exists=True))
@click.argument('svg_path', type=click.Path(exists=True))
@click.option(
    '--page',
    type=int,
    default=0,
    help='Page number to sign (0-indexed). Default: 0'
)
@click.option(
    '--x',
    type=float,
    default=100.0,
    help='Horizontal coordinate for signature placement. Default: 100.0'
)
@click.option(
    '--y',
    type=float,
    default=100.0,
    help='Vertical coordinate for signature placement. Default: 100.0'
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    help='Output PDF path. If not specified, overwrites the input PDF.'
)
def main(pdf_path: str, svg_path: str, page: int, x: float, y: float, output: str) -> None:
    """Sign a PDF document with an SVG signature.
    
    PDF_PATH: Path to the PDF document to be signed.
    SVG_PATH: Path to the SVG file containing the signature.
    """
    pass


if __name__ == '__main__':
    main()
