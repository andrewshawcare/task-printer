import os
from escpos import escpos, printer
from tempfile import NamedTemporaryFile
from get_auth_token import get_auth_token
from get_focus_tasks import get_focus_tasks
from print_html_file import print_html_file
from string import Template
import markdown

username = os.getenv("NIRVANA_USERNAME")
if not username:
    raise ValueError("NIRVANA_USERNAME environment variable is not set")
password = os.getenv("NIRVANA_PASSWORD")
if not password:
    raise ValueError("NIRVANA_PASSWORD environment variable is not set")

authtoken = get_auth_token(username, password)

focus_tasks = get_focus_tasks(authtoken)

if not focus_tasks:
    raise ValueError("No focus tasks found")

for task in focus_tasks:
    print(task)

next_focus_task = focus_tasks[0]

with open("./task.html", "r") as task_template_file:
    task_template = task_template_file.read()

task_content = Template(task_template).substitute(
    title=next_focus_task["name"],
    description=markdown.markdown(next_focus_task["note"]),
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
