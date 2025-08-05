def print_task_from_file(file_path, printer):
    """Read a task from a file and print it using the provided printer."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Print each line
    for line in content.splitlines():
        printer.textln(line)