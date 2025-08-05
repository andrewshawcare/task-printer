from escpos import printer
from tempfile import NamedTemporaryFile
from print_task_from_text_file.main import print_task_from_text_file

vendor_id = 0x04b8 # Seiko Epson Corp.
product_id = 0x0e28 # TM-T20III

usb_printer = printer.Usb(
    idVendor=vendor_id,
    idProduct=product_id
)

task_content = "Task: Implement TDD for thermal printer\n- Write failing test\n- Make it pass\n- Refactor"

with NamedTemporaryFile(delete_on_close=False) as task_file:
    task_file.write(task_content.encode())
    task_file.close()

    print_task_from_text_file(task_file.name, usb_printer)
    usb_printer.close()
