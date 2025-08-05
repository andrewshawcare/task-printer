import pytest
from escpos.printer import Dummy
from pathlib import Path
import tempfile
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
from task_printer import print_task_from_file


def test_should_print_task_from_file():
    """Test that a task can be read from a file and printed."""
    # Arrange
    dummy_printer = Dummy()
    
    # Create a temporary file with test content
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        test_content = "This is a test task\nWith multiple lines"
        f.write(test_content)
        temp_file_path = f.name
    
    try:
        # Act
        print_task_from_file(temp_file_path, dummy_printer)
        
        # Assert
        output = dummy_printer.output
        assert b"This is a test task" in output
        assert b"With multiple lines" in output
        
    finally:
        # Cleanup
        Path(temp_file_path).unlink()


def test_should_handle_empty_file():
    """Test that an empty file can be processed without errors."""
    # Arrange
    dummy_printer = Dummy()
    
    # Create an empty temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        temp_file_path = f.name
    
    try:
        # Act
        print_task_from_file(temp_file_path, dummy_printer)
        
        # Assert - no content should be printed
        output = dummy_printer.output
        assert output == b""
        
    finally:
        # Cleanup
        Path(temp_file_path).unlink()


def test_should_raise_error_for_nonexistent_file():
    """Test that a FileNotFoundError is raised for a nonexistent file."""
    # Arrange
    dummy_printer = Dummy()
    nonexistent_file = "/tmp/this_file_does_not_exist_12345.txt"
    
    # Act & Assert
    with pytest.raises(FileNotFoundError):
        print_task_from_file(nonexistent_file, dummy_printer)