from jsonschema_typed import JSONSchema
import requests


def get_focus_tasks(authtoken: str, since: int = 0) -> list:
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
