import os
import sys

import requests
from dotenv import load_dotenv


load_dotenv()

GITLAB_URL = os.getenv("GITLAB_URL")
GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")
GITLAB_PROJECT_ID = os.getenv("GITLAB_PROJECT_ID")


def test_gitlab_connection():
    """Test authentication with the GitLab API."""

    if not GITLAB_URL:
        print("Error: GITLAB_URL is not set.")
        return

    if not GITLAB_TOKEN:
        print("Error: GITLAB_TOKEN is not set.")
        return

    url = f"{GITLAB_URL}/api/v4/user"

    headers = {
        "PRIVATE-TOKEN": GITLAB_TOKEN
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            user = response.json()

            print("GitLab API connection successful!")
            print(f"Username: {user['username']}")
            print(f"User ID: {user['id']}")

        elif response.status_code == 401:
            print("Error: GitLab authentication failed.")

        else:
            print(
                f"Error: GitLab API returned "
                f"status {response.status_code}"
            )

    except requests.exceptions.RequestException as error:
        print(f"Error connecting to GitLab: {error}")

def get_project():
    """Retrieve and display GitLab project information."""

    if not GITLAB_PROJECT_ID:
        print("Error: GITLAB_PROJECT_ID is not set.")
        return

    url = f"{GITLAB_URL}/api/v4/projects/{GITLAB_PROJECT_ID}"

    headers = {
        "PRIVATE-TOKEN": GITLAB_TOKEN
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            project = response.json()

            print("\nProject Information")
            print("-------------------")
            print(f"Project Name: {project['name']}")
            print(f"Project ID: {project['id']}")
            print(f"Default Branch: {project['default_branch']}")
            print(f"Project URL: {project['web_url']}")

        elif response.status_code == 401:
            print("Error: GitLab authentication failed.")

        elif response.status_code == 404:
            print("Error: Project not found.")

        else:
            print(
                f"Error: GitLab API returned "
                f"status {response.status_code}"
            )

    except requests.exceptions.RequestException as error:
        print(f"Error connecting to GitLab: {error}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python gitlab_analyzer.py <command>")
        print("Available commands: project")
        return

    command = sys.argv[1]

    if command == "project":
        get_project()
    else:
        print(f"Error: Unknown command '{command}'")
        print("Available commands: project")


if __name__ == "__main__":
    main()