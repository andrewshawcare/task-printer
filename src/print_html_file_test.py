import pytest
from pathlib import Path
from escpos.printer import Dummy
from escpos.constants import PAPER_FULL_CUT
from tempfile import NamedTemporaryFile
from .print_html_file import print_html_file


def assert_image_output(output: bytes):
    """Helper function to assert that output contains image data"""
    BIT_IMAGE_RASTER_COMMAND = b"\x1dv0"  # GS v 0
    GRAPHICS_COMMAND = b"\x1d(L"  # GS ( L
    BIT_IMAGE_COLUMN_COMMAND = b"\x1b*"  # ESC *

    assert (
        BIT_IMAGE_RASTER_COMMAND in output
        or GRAPHICS_COMMAND in output
        or BIT_IMAGE_COLUMN_COMMAND in output
    ), "Output does not contain expected image data commands"


html_content_list: list[str] = [
    "<html><body><h1>First Task</h1></body></html>",
    "<html><body><h1>Second Task</h1></body></html>",
]


def test_should_print_an_html_file():
    """It should read an HTML file and print it as an image"""

    # Arrange
    printer = Dummy()
    html_content_bytes = html_content_list[0].encode()

    with NamedTemporaryFile(suffix=".html", delete_on_close=False) as html_file:
        html_file.write(html_content_bytes)
        html_file.close()

        # Act
        print_html_file(Path(html_file.name), printer)

    # Assert
    output = printer.output
    assert_image_output(output)
    assert PAPER_FULL_CUT in output


def test_should_accept_string_path():
    """It should accept string paths"""

    # Arrange
    printer = Dummy()
    html_content_bytes = html_content_list[0].encode()

    with NamedTemporaryFile(suffix=".html", delete_on_close=False) as html_file:
        html_file.write(html_content_bytes)
        html_file.close()

        # Act
        print_html_file(html_file.name, printer)

    # Assert
    output = printer.output
    assert_image_output(output)
    assert PAPER_FULL_CUT in output


def test_should_raise_error_for_nonexistent_file():
    """It should raise an error for a nonexistent file"""
    # Arrange
    printer = Dummy()
    nonexistent_file = Path("nonexistent_file.html")

    # Act & Assert
    with pytest.raises(FileNotFoundError):
        print_html_file(nonexistent_file, printer)


def test_should_read_html_content_and_convert_to_image():
    """It should read the HTML content and convert it to an image"""
    # Arrange
    printer = Dummy()

    with NamedTemporaryFile(suffix=".html", delete_on_close=False) as html_file:
        html_file.write(html_content_list[0].encode())
        html_file.close()

        # Act
        print_html_file(Path(html_file.name), printer)

    # Assert
    output = printer.output
    assert_image_output(output)

    # Arbitrary minimum size for image data
    minimum_image_size_in_bytes = 100
    assert len(output) > minimum_image_size_in_bytes

    assert PAPER_FULL_CUT in output


def test_should_render_different_html_content_differently():
    """It should render different HTML content differently"""
    # Arrange
    printer1 = Dummy()
    printer2 = Dummy()

    # Act
    with NamedTemporaryFile(suffix=".html", delete_on_close=False) as html_file:
        html_file.write(html_content_list[0].encode())
        html_file.close()
        print_html_file(Path(html_file.name), printer1)

    with NamedTemporaryFile(suffix=".html", delete_on_close=False) as html_file:
        html_file.write(html_content_list[1].encode())
        html_file.close()
        print_html_file(Path(html_file.name), printer2)

    # Assert
    output1 = printer1.output
    output2 = printer2.output

    # Both should have image data
    assert_image_output(output1)
    assert_image_output(output2)

    assert output1 != output2, "Outputs for different HTML content should differ"
