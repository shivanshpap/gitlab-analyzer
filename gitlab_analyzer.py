import os
import sys

import requests
from dotenv import load_dotenv


load_dotenv()

GITLAB_URL = os.getenv("GITLAB_URL")
GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")
GITLAB_PROJECT_ID = os.getenv("GITLAB_PROJECT_ID")
GITLAB_BRANCH = os.getenv("GITLAB_BRANCH", "main")


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

def get_latest_pipeline():
    """Retrieve the latest pipeline for the configured branch."""

    url = f"{GITLAB_URL}/api/v4/projects/{GITLAB_PROJECT_ID}/pipelines"

    headers = {
        "PRIVATE-TOKEN": GITLAB_TOKEN
    }

    params = {
        "ref": GITLAB_BRANCH,
        "per_page": 1
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=10
        )

        if response.status_code == 200:
            pipelines = response.json()

            if not pipelines:
                print(
                    f"No pipelines found for branch "
                    f"'{GITLAB_BRANCH}'."
                )
                return

            pipeline = pipelines[0]
            pipeline_id = pipeline["id"]

            details_url = (
                f"{GITLAB_URL}/api/v4/projects/"
                f"{GITLAB_PROJECT_ID}/pipelines/{pipeline_id}"
            )

            details_response = requests.get(
                details_url,
                headers=headers,
                timeout=10
            )

            if details_response.status_code != 200:
                print(
                    f"Error retrieving pipeline details: "
                    f"status {details_response.status_code}"
                )
                return

            pipeline_details = details_response.json()

            print("\nLatest Pipeline")
            print("---------------")
            print(f"Pipeline ID: {pipeline_details['id']}")
            print(f"Status: {pipeline_details['status']}")
            print(f"Branch: {pipeline_details['ref']}")
            print(f"Commit: {pipeline_details['sha']}")

            duration = pipeline_details.get("duration")

            if duration is not None:
                minutes = int(duration // 60)
                seconds = int(duration % 60)
                print(f"Duration: {minutes}m {seconds}s")
            else:
                print("Duration: Not available")

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
        print("Available commands: project, pipeline")
        return

    command = sys.argv[1]

    if command == "project":
        get_project()
    elif command == "pipeline":
        get_latest_pipeline()
    else:
        print(f"Error: Unknown command '{command}'")
        print("Available commands: project, pipeline")


if __name__ == "__main__":
    main()