from escpos import printer

vendor_id = 0x04b8 # Seiko Epson Corp.
product_id = 0x0e28 # TM-T20III

usb_printer = printer.Usb(vendor_id, product_id)

usb_printer.textln("Hello, World!")
usb_printer.cut()

usb_printer.close()
