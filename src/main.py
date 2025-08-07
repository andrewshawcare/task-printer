import os
from escpos import escpos, printer
from tempfile import NamedTemporaryFile
from print_html_file import print_html_file
from string import Template
import requests
import markdown
import re
from jsonschema_typed import JSONSchema


def get_auth_token(username: str, password: str) -> str:
    login_url = "https://focus.nirvanahq.com/login"

    login_data = {"u": username, "p": password}

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(login_url, data=login_data, headers=headers)
    response.raise_for_status()

    # Extract authtoken from the JavaScript in the HTML response
    # Look for: authtoken = "...";
    match = re.search(r'authtoken\s*=\s*"([^"]+)"', response.text)
    if match:
        return match.group(1)

    raise ValueError("Could not find authtoken in login response")


def get_tasks(authtoken: str, since: int = 0) -> list:
    tasks = []

    url = f"https://gc-api.nirvanahq.com/api/everything?&return=everything&since={since}&authtoken={authtoken}"

    response = requests.get(url)
    response.raise_for_status()

    response_json: JSONSchema["everything.json"] = response.json()
    results = response_json["results"]

    if results:
        for item in results:
            if "task" in item and item["task"] is not None:
                task = item["task"]
                if (
                    task.get("completed", "1") == "0"
                    and task.get("deleted", "1") == "0"
                    and task.get("cancelled", "1") == "0"
                    and task.get("seqt", "0") != "0"
                ):
                    tasks.append(task)

    tasks.sort(key=lambda task: int(task.get("seqt", 0)))

    return tasks


username = os.getenv("NIRVANA_USERNAME")
if not username:
    raise ValueError("NIRVANA_USERNAME environment variable is not set")
password = os.getenv("NIRVANA_PASSWORD")
if not password:
    raise ValueError("NIRVANA_PASSWORD environment variable is not set")

authtoken = get_auth_token(username, password)

with open("./task.html", "r") as task_template_file:
    task_template = task_template_file.read()

tasks = get_tasks(authtoken)

if not tasks:
    raise ValueError("No tasks found")

next_task = tasks[0]

task_content = Template(task_template).substitute(
    title=next_task["name"], description=markdown.markdown(next_task["note"])
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
