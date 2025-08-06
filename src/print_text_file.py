from escpos.escpos import Escpos
from pathlib import Path
from typing import Union


def print_text_file(file_path: Union[str, Path], printer: Escpos) -> None:
    """Print a task from a text file to the specified printer."""
    if isinstance(file_path, str):
        file_path = Path(file_path)

    content = file_path.read_text()

    printer.text(content)

    printer.cut()
