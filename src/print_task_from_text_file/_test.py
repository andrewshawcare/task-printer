import pytest
from pathlib import Path
from escpos.printer import Dummy
from escpos.constants import PAPER_FULL_CUT
from tempfile import NamedTemporaryFile
from src.print_task_from_text_file.main import print_task_from_text_file


def test_should_print_task_from_text_file():
    """Test that print_task_from_text_file reads a file and prints its content"""

    # Arrange
    printer = Dummy()
    task_content = "Complete the TDD implementation"
    
    with NamedTemporaryFile(delete_on_close=False) as task_file:
        task_file.write(task_content.encode())
        task_file.close()

        # Act
        print_task_from_text_file(Path(task_file.name), printer)
        
    # Assert
    output = printer.output
    
    assert task_content.encode() in output
    assert PAPER_FULL_CUT in output


def test_should_accept_string_path():
    """Test that print_task_from_file accepts string paths"""
    
    # Arrange
    printer = Dummy()
    task_content = "Complete the TDD implementation"

    # Act
    with NamedTemporaryFile(delete_on_close=False) as task_file:
        task_file.write(task_content.encode())
        task_file.close()

        # Act
        print_task_from_text_file(task_file.name, printer)

    # Assert
    output = printer.output
    assert task_content.encode() in output
    assert PAPER_FULL_CUT in output
        


def test_should_raise_error_for_nonexistent_file():
    """Test that print_task_from_file raises error for nonexistent file"""
    # Arrange
    printer = Dummy()
    nonexistent_file = Path("nonexistent_file.txt")
    
    # Act & Assert
    with pytest.raises(FileNotFoundError):
        print_task_from_text_file(nonexistent_file, printer)