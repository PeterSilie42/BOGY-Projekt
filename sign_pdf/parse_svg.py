"""Parse SVG files containing signatures and extract path information.

This module handles reading and parsing SVG files to extract signature
paths and their properties for use in rendering to PDF documents.
"""

import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import List
import re


@dataclass
class DrawCommand:
    """Represents a single SVG path drawing command."""
    command: str
    parameters: List[float]


@dataclass
class BoundingBox:
    """Represents the bounding box of an SVG."""
    x: float
    y: float
    width: float
    height: float


@dataclass
class PathData:
    """Represents parsed SVG path data with styling."""
    stroke: str
    stroke_width: float
    d: List[DrawCommand]


@dataclass
class SVGData:
    """Complete parsed SVG data with signature and helpline paths."""
    bounding_box: BoundingBox
    signature: PathData
    helpline: PathData


def _parse_svg_path_d(d_string: str) -> List[DrawCommand]:
    """Parse the d attribute of an SVG path into drawing commands.
    
    The d attribute uses a mini-language with single-letter commands followed
    by numeric parameters. Supported commands:
    - M/m: moveto
    - L/l: lineto
    - H/h: horizontal lineto
    - V/v: vertical lineto
    - C/c: cubic Bézier curveto
    - S/s: smooth cubic Bézier curveto
    - Q/q: quadratic Bézier curveto
    - T/t: smooth quadratic Bézier curveto
    - A/a: elliptical Arc
    - Z/z: closepath
    
    Args:
        d_string: The SVG path d attribute string.
        
    Returns:
        A list of DrawCommand objects.
    """
    commands = []
    
    # Pattern to match command letters and their following numbers
    # Handles numbers in various formats: integers, decimals, scientific notation
    pattern = r'([MmLlHhVvCcSsQqTtAaZz])|(-?\d+\.?\d*(?:[eE][+-]?\d+)?)'
    
    tokens = re.findall(pattern, d_string)
    
    current_command = None
    current_params = []
    
    for token_cmd, token_num in tokens:
        if token_cmd:
            # This is a command letter
            if current_command is not None and current_params:
                # Save the previous command
                commands.append(DrawCommand(command=current_command, parameters=current_params))
            current_command = token_cmd
            current_params = []
        else:
            # This is a number
            current_params.append(float(token_num))
    
    # Don't forget the last command
    if current_command is not None and current_params:
        commands.append(DrawCommand(command=current_command, parameters=current_params))
    elif current_command is not None:
        # Handle commands with no parameters like 'Z'
        commands.append(DrawCommand(command=current_command, parameters=[]))
    
    return commands


def _extract_path_data(path_element) -> PathData:
    """Extract stroke, stroke_width, and path commands from a path element.
    
    Args:
        path_element: An ElementTree Element representing a path.
        
    Returns:
        A PathData object with styling and drawing commands.
        
    Raises:
        ValueError: If the path element doesn't have a d attribute.
    """
    d_attr = path_element.get('d')
    if not d_attr:
        raise ValueError("Path element missing 'd' attribute")
    
    # Get stroke color, default to black
    stroke = path_element.get('stroke', 'black')
    
    # Get stroke width, default to 1
    stroke_width_str = path_element.get('stroke-width', '1')
    try:
        stroke_width = float(stroke_width_str)
    except ValueError:
        stroke_width = 1
    
    # Parse the path d attribute
    commands = _parse_svg_path_d(d_attr)
    
    return PathData(stroke=stroke, stroke_width=stroke_width, d=commands)


def parse_svg(svg_path: str) -> SVGData:
    """Parse an SVG file and extract signature path data.
    
    Reads an SVG file and extracts:
    - The bounding box (from viewBox or width/height attributes)
    - The signature path (path with id='signature')
    - The helpline path (path with id='helpline')
    
    Args:
        svg_path: Path to the SVG file containing the signature.
        
    Returns:
        An SVGData dataclass containing the parsed SVG information.
        
    Raises:
        FileNotFoundError: If the SVG file does not exist.
        ValueError: If the SVG file is invalid, malformed, or missing required paths.
    """
    # Check if file exists
    svg_file = Path(svg_path)
    if not svg_file.exists():
        raise FileNotFoundError(f"SVG file '{svg_path}' could not be found")
    
    # Parse the XML
    try:
        tree = ET.parse(svg_file)
        root = tree.getroot()
    except ET.ParseError as e:
        raise ValueError(f"Failed to parse XML in '{svg_path}': {e}")
    
    # Extract bounding box from viewBox or width/height
    viewbox = root.get('viewBox')
    if viewbox:
        try:
            x, y, width, height = map(float, viewbox.split())
            bbox = BoundingBox(x=x, y=y, width=width, height=height)
        except (ValueError, AttributeError):
            raise ValueError(f"Invalid viewBox in SVG: {viewbox}")
    else:
        # Fall back to width and height attributes
        try:
            width = float(root.get('width', 100))
            height = float(root.get('height', 100))
            bbox = BoundingBox(x=0, y=0, width=width, height=height)
        except ValueError:
            raise ValueError("SVG missing valid viewBox and width/height attributes")
    
    # Find signature and helpline paths
    # Need to handle XML namespaces properly
    namespace = {'svg': 'http://www.w3.org/2000/svg'}
    
    signature_elem = None
    helpline_elem = None
    
    # Try to find paths with id attribute
    for path in root.findall('.//svg:path', namespace):
        path_id = path.get('id')
        if path_id == 'signature':
            signature_elem = path
        elif path_id == 'helpline':
            helpline_elem = path
    
    # If namespace search didn't work, try without namespace
    if signature_elem is None or helpline_elem is None:
        for path in root.findall('.//path'):
            path_id = path.get('id')
            if path_id == 'signature':
                signature_elem = path
            elif path_id == 'helpline':
                helpline_elem = path
    
    if signature_elem is None:
        raise ValueError("SVG file must contain a path with id='signature'")
    if helpline_elem is None:
        raise ValueError("SVG file must contain a path with id='helpline'")
    
    # Extract path data
    try:
        signature = _extract_path_data(signature_elem)
    except ValueError as e:
        raise ValueError(f"Error parsing signature path: {e}")
    
    try:
        helpline = _extract_path_data(helpline_elem)
    except ValueError as e:
        raise ValueError(f"Error parsing helpline path: {e}")
    
    return SVGData(bounding_box=bbox, signature=signature, helpline=helpline)
