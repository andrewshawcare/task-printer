import pytest
from pathlib import Path
from escpos.printer import Dummy
from tempfile import NamedTemporaryFile
from .print_text_file import print_text_file


def test_should_print_text_file():
    """It should read a file and print its content"""

    # Arrange
    printer = Dummy()
    task_content = "Lorem ipsum dolor sit amet"

    with NamedTemporaryFile(delete_on_close=False) as task_file:
        task_file.write(task_content.encode())
        task_file.close()

        # Act
        print_text_file(Path(task_file.name), printer)

    # Assert
    output = printer.output

    assert task_content.encode() in output


def test_should_accept_string_path():
    """It should accept string paths"""

    # Arrange
    printer = Dummy()
    task_content = "Lorem ipsum dolor sit amet"

    # Act
    with NamedTemporaryFile(delete_on_close=False) as task_file:
        task_file.write(task_content.encode())
        task_file.close()

        # Act
        print_text_file(task_file.name, printer)

    # Assert
    output = printer.output
    assert task_content.encode() in output


def test_should_raise_error_for_nonexistent_file():
    """It should raise an error for a nonexistent file"""
    # Arrange
    printer = Dummy()
    nonexistent_file = Path("nonexistent_file.txt")

    # Act & Assert
    with pytest.raises(FileNotFoundError):
        print_text_file(nonexistent_file, printer)
