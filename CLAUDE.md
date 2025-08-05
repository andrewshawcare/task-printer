# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python project that interfaces with Epson TM-T20III thermal printers via USB using the python-escpos library.

## Development Environment

- Python 3.12+ required
- Uses `uv` package manager (version 0.8.4+)
- Virtual environment at `.venv/`

## Essential Commands

```bash
# Install dependencies
uv sync

# Run the printer application
uv run src/main.py
```

## Architecture

The project is a simple thermal printer interface:
- `src/main.py`: Main application that connects to an Epson TM-T20III printer via USB (vendor_id: 0x04b8, product_id: 0x0e28)
- Uses `python-escpos[usb]` library for printer communication
- Type stubs are provided in `typings/escpos/` for better IDE support

## Key Dependencies

- `python-escpos[usb]`: Core library for ESC/POS printer communication
- `pyusb`: USB device communication (dependency of python-escpos)
- `pillow`: Image processing capabilities for printing images