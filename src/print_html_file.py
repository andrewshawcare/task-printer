from tempfile import NamedTemporaryFile
from escpos.escpos import Escpos
from pathlib import Path
from typing import Union
import imgkit


def print_html_file(file_path: Union[str, Path], printer: Escpos) -> None:
    """Print an HTML file as an image to the specified printer."""
    if isinstance(file_path, str):
        file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    html_content = file_path.read_text()
    format = "png"

    with NamedTemporaryFile(suffix=f".{format}", delete_on_close=False) as img_file:
        imgkit.api.from_string(
            string=html_content,
            output_path=img_file.name,
            options={"format": format, "width": 576},
        )
        printer.image(img_source=img_file.name)
