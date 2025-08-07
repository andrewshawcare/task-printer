import re
import requests


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
