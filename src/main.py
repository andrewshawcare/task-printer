from escpos import escpos, printer
from tempfile import NamedTemporaryFile
from print_html_file import print_html_file
from string import Template

with open("./task.html", "r") as task_template_file:
    task_template = task_template_file.read()

task = {"title": "Task", "description": "Complete the TDD implementation"}

task_content = Template(task_template).substitute(
    title=task["title"], description=task["description"]
)

# Seiko Epson Corp.
vendor_id = 0x04B8

# TM-T20III
product_id = 0x0E28

with (
    NamedTemporaryFile(suffix=".html", delete_on_close=False) as task_file,
    escpos.EscposIO(
        printer.Usb(idVendor=vendor_id, idProduct=product_id)
    ) as printer_io,
):
    task_file.write(task_content.encode())
    task_file.close()

    print_html_file(task_file.name, printer_io.printer)
