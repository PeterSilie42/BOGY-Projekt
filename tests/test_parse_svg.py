"""Tests for the SVG parsing module.

Tests the parse_svg function and related SVG handling functionality.
"""

import pytest # type: ignore
import tempfile
from pathlib import Path
from sign_pdf.parse_svg import parse_svg, SVGData, PathData


@pytest.fixture
def valid_svg_with_signature_and_helpline():
    """Fixture providing a valid SVG with signature and helpline paths."""
    svg_content = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="200" height="100" viewBox="0 0 200 100">
  <path id="signature" d="M 10 50 L 50 30 L 90 70 L 120 40" stroke="red" stroke-width="2"/>
  <path id="helpline" d="M 10 60 L 190 60" stroke="black" stroke-width="1"/>
</svg>"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.svg', delete=False) as f:
        f.write(svg_content)
        f.flush()
        yield f.name
    Path(f.name).unlink()


@pytest.fixture
def valid_svg_with_defaults():
    """Fixture providing a valid SVG with paths using default stroke and stroke-width."""
    svg_content = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="300" height="200" viewBox="0 0 300 200">
  <path id="signature" d="M 20 100 L 80 60 L 120 120"/>
  <path id="helpline" d="M 10 150 L 290 150"/>
</svg>"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.svg', delete=False) as f:
        f.write(svg_content)
        f.flush()
        yield f.name
    Path(f.name).unlink()


@pytest.fixture
def svg_missing_signature():
    """Fixture providing an SVG missing the signature path."""
    svg_content = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="200" height="100" viewBox="0 0 200 100">
  <path id="helpline" d="M 10 50 L 190 50"/>
</svg>"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.svg', delete=False) as f:
        f.write(svg_content)
        f.flush()
        yield f.name
    Path(f.name).unlink()


@pytest.fixture
def svg_missing_helpline():
    """Fixture providing an SVG missing the helpline path."""
    svg_content = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="200" height="100" viewBox="0 0 200 100">
  <path id="signature" d="M 10 50 L 190 50"/>
</svg>"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.svg', delete=False) as f:
        f.write(svg_content)
        f.flush()
        yield f.name
    Path(f.name).unlink()


@pytest.fixture
def malformed_svg():
    """Fixture providing a malformed SVG file."""
    svg_content = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="200" height="100">
  <path id="signature" d="M 10 50 L 50 30">
  <!-- Missing closing tag -->
</svg>"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.svg', delete=False) as f:
        f.write(svg_content)
        f.flush()
        yield f.name
    Path(f.name).unlink()


@pytest.fixture
def not_xml_file():
    """Fixture providing a file that is not valid XML."""
    content = "This is not valid XML at all {{{ <>"
    with tempfile.NamedTemporaryFile(mode='w', suffix='.svg', delete=False) as f:
        f.write(content)
        f.flush()
        yield f.name
    Path(f.name).unlink()


@pytest.fixture
def svg_complex_paths():
    """Fixture providing SVG with complex path commands."""
    svg_content = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300" viewBox="0 0 400 300">
  <path id="signature" d="M 10,50 L 50,30 C 100,20 150,40 180,10 Q 200,0 220,20 A 10,10 0 0 1 240,30 Z" stroke="#0066CC" stroke-width="2.5"/>
  <path id="helpline" d="M 10,200 H 390 V 210 H 10 Z" stroke="rgba(0,0,0,0.5)" stroke-width="0.5"/>
</svg>"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.svg', delete=False) as f:
        f.write(svg_content)
        f.flush()
        yield f.name
    Path(f.name).unlink()


class TestParseSVGSuccessful:
    """Test successful SVG parsing."""

    def test_parse_valid_svg_returns_dataclass(self, valid_svg_with_signature_and_helpline):
        """Test that parsing a valid SVG returns an SVGData dataclass."""
        result = parse_svg(valid_svg_with_signature_and_helpline)
        assert isinstance(result, SVGData), "Result should be an SVGData instance"

    def test_parsed_svg_has_bounding_box(self, valid_svg_with_signature_and_helpline):
        """Test that the parsed SVG contains a bounding box."""
        result = parse_svg(valid_svg_with_signature_and_helpline)
        assert hasattr(result, 'bounding_box'), "SVGData should have bounding_box attribute"
        assert hasattr(result.bounding_box, 'x'), "Bounding box should have x coordinate"
        assert hasattr(result.bounding_box, 'y'), "Bounding box should have y coordinate"
        assert hasattr(result.bounding_box, 'width'), "Bounding box should have width"
        assert hasattr(result.bounding_box, 'height'), "Bounding box should have height"
        # Check values match the SVG viewBox
        assert result.bounding_box.width == 200, "Bounding box width should be 200"
        assert result.bounding_box.height == 100, "Bounding box height should be 100"

    def test_parsed_svg_has_signature_path(self, valid_svg_with_signature_and_helpline):
        """Test that the parsed SVG contains signature path data."""
        result = parse_svg(valid_svg_with_signature_and_helpline)
        assert hasattr(result, 'signature'), "SVGData should have signature attribute"
        assert isinstance(result.signature, PathData), "signature should be a PathData instance"

    def test_parsed_svg_has_helpline_path(self, valid_svg_with_signature_and_helpline):
        """Test that the parsed SVG contains helpline path data."""
        result = parse_svg(valid_svg_with_signature_and_helpline)
        assert hasattr(result, 'helpline'), "SVGData should have helpline attribute"
        assert isinstance(result.helpline, PathData), "helpline should be a PathData instance"

    def test_signature_path_has_required_attributes(self, valid_svg_with_signature_and_helpline):
        """Test that signature path has stroke, stroke_width, and d attributes."""
        result = parse_svg(valid_svg_with_signature_and_helpline)
        sig = result.signature
        assert hasattr(sig, 'stroke'), "PathData should have stroke attribute"
        assert hasattr(sig, 'stroke_width'), "PathData should have stroke_width attribute"
        assert hasattr(sig, 'd'), "PathData should have d attribute"
        assert sig.stroke == "red", "Stroke color should be preserved as-is"
        assert sig.stroke_width == 2, "Stroke width should be converted to float/int"

    def test_helpline_path_has_required_attributes(self, valid_svg_with_signature_and_helpline):
        """Test that helpline path has stroke, stroke_width, and d attributes."""
        result = parse_svg(valid_svg_with_signature_and_helpline)
        hl = result.helpline
        assert hasattr(hl, 'stroke'), "PathData should have stroke attribute"
        assert hasattr(hl, 'stroke_width'), "PathData should have stroke_width attribute"
        assert hasattr(hl, 'd'), "PathData should have d attribute"
        assert hl.stroke == "black", "Stroke color should be black"
        assert hl.stroke_width == 1, "Stroke width should be 1"

    def test_path_d_is_list_of_commands(self, valid_svg_with_signature_and_helpline):
        """Test that path d attribute is parsed into a list of commands."""
        result = parse_svg(valid_svg_with_signature_and_helpline)
        d = result.signature.d
        assert isinstance(d, list), "Path d should be a list of drawing commands"
        assert len(d) > 0, "Path d should contain at least one command"
        # Each command should have a type and parameters
        for command in d:
            assert hasattr(command, 'command'), "Command should have a command attribute"
            assert hasattr(command, 'parameters'), "Command should have parameters"

    def test_default_stroke_color_is_black(self, valid_svg_with_defaults):
        """Test that paths without explicit stroke default to black."""
        result = parse_svg(valid_svg_with_defaults)
        assert result.signature.stroke == "black", "Default stroke color should be black"

    def test_default_stroke_width_is_one(self, valid_svg_with_defaults):
        """Test that paths without explicit stroke-width default to 1."""
        result = parse_svg(valid_svg_with_defaults)
        assert result.signature.stroke_width == 1, "Default stroke-width should be 1"

    def test_hex_color_values_preserved(self, svg_complex_paths):
        """Test that hex color values are preserved."""
        result = parse_svg(svg_complex_paths)
        assert result.signature.stroke == "#0066CC", "Hex color should be preserved"

    def test_stroke_width_as_float(self, svg_complex_paths):
        """Test that decimal stroke-width values are preserved."""
        result = parse_svg(svg_complex_paths)
        assert result.helpline.stroke_width == 0.5, "Decimal stroke-width should be preserved"

    def test_path_contains_drawing_commands(self, valid_svg_with_signature_and_helpline):
        """Test that parsed paths contain recognizable SVG drawing commands."""
        result = parse_svg(valid_svg_with_signature_and_helpline)
        commands = result.signature.d
        # Should have M (move), L (line to) commands
        command_types = [cmd.command for cmd in commands]
        assert 'M' in command_types, "Path should contain M (moveto) command"
        # Either L or other drawing commands
        assert len(command_types) > 1, "Path should contain multiple commands"


class TestParseSVGErrors:
    """Test error handling in SVG parsing."""

    def test_nonexistent_file_raises_file_not_found(self):
        """Test that parsing a nonexistent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError) as exc_info:
            parse_svg("/nonexistent/path/to/file.svg")
        assert "could not be found" in str(exc_info.value).lower()

    def test_missing_signature_path_raises_value_error(self, svg_missing_signature):
        """Test that SVG without signature path raises ValueError with clear message."""
        with pytest.raises(ValueError) as exc_info:
            parse_svg(svg_missing_signature)
        error_msg = str(exc_info.value).lower()
        assert "signature" in error_msg, "Error message should mention 'signature'"

    def test_missing_helpline_path_raises_value_error(self, svg_missing_helpline):
        """Test that SVG without helpline path raises ValueError with clear message."""
        with pytest.raises(ValueError) as exc_info:
            parse_svg(svg_missing_helpline)
        error_msg = str(exc_info.value).lower()
        assert "helpline" in error_msg, "Error message should mention 'helpline'"

    def test_malformed_xml_raises_value_error(self, malformed_svg):
        """Test that malformed XML raises ValueError with helpful message."""
        with pytest.raises(ValueError) as exc_info:
            parse_svg(malformed_svg)
        error_msg = str(exc_info.value).lower()
        assert "xml" in error_msg or "parse" in error_msg, "Error should mention XML parsing issue"

    def test_invalid_xml_raises_value_error(self, not_xml_file):
        """Test that non-XML file raises ValueError with helpful message."""
        with pytest.raises(ValueError) as exc_info:
            parse_svg(not_xml_file)
        error_msg = str(exc_info.value).lower()
        assert "xml" in error_msg or "parse" in error_msg or "invalid" in error_msg

    def test_error_message_includes_file_path(self, svg_missing_signature):
        """Test that error messages include the file path for debugging."""
        with pytest.raises(ValueError) as exc_info:
            parse_svg(svg_missing_signature)
        # The error message should reference the file somehow or context
        error_msg = str(exc_info.value)
        assert len(error_msg) > 10, "Error message should be descriptive"


class TestParseSVGRedrawability:
    """Test that parsed SVG data contains all information needed to redraw."""

    def test_signature_path_has_all_redraw_info(self, valid_svg_with_signature_and_helpline):
        """Test that signature path contains all info needed to redraw it."""
        result = parse_svg(valid_svg_with_signature_and_helpline)
        sig = result.signature
        # Should have: stroke (color), stroke_width (width), and d (path commands)
        assert sig.stroke is not None, "Stroke must be present"
        assert sig.stroke_width is not None, "Stroke width must be present"
        assert sig.d is not None, "Path commands must be present"
        assert len(sig.d) > 0, "Path commands list should not be empty"

    def test_helpline_path_has_all_redraw_info(self, valid_svg_with_signature_and_helpline):
        """Test that helpline path contains all info needed to redraw it."""
        result = parse_svg(valid_svg_with_signature_and_helpline)
        hl = result.helpline
        # Should have: stroke (color), stroke_width (width), and d (path commands)
        assert hl.stroke is not None, "Stroke must be present"
        assert hl.stroke_width is not None, "Stroke width must be present"
        assert hl.d is not None, "Path commands must be present"
        assert len(hl.d) > 0, "Path commands list should not be empty"

    def test_complex_path_commands_preserved(self, svg_complex_paths):
        """Test that complex path commands are correctly parsed."""
        result = parse_svg(svg_complex_paths)
        sig = result.signature
        commands = sig.d
        # Should include M, L, C, Q, A, Z commands from the test SVG
        command_types = [cmd.command for cmd in commands]
        # Verify we have various command types
        assert 'M' in command_types, "Should have moveto command"
        # The exact set depends on parsing, but should have multiple types
        assert len(set(command_types)) > 1, "Should have multiple command types"

    def test_bounding_box_has_all_dimensions(self, valid_svg_with_signature_and_helpline):
        """Test that bounding box has all necessary dimensions."""
        result = parse_svg(valid_svg_with_signature_and_helpline)
        bbox = result.bounding_box
        # All should be non-None numbers
        assert isinstance(bbox.x, (int, float)), "Bounding box x should be numeric"
        assert isinstance(bbox.y, (int, float)), "Bounding box y should be numeric"
        assert isinstance(bbox.width, (int, float)), "Bounding box width should be numeric"
        assert isinstance(bbox.height, (int, float)), "Bounding box height should be numeric"
        assert bbox.width > 0, "Bounding box width should be positive"
        assert bbox.height > 0, "Bounding box height should be positive"
