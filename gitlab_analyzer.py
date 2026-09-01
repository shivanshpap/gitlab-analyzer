import os

import requests
from dotenv import load_dotenv


load_dotenv()

GITLAB_URL = os.getenv("GITLAB_URL")
GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")


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


def main():
    test_gitlab_connection()


if __name__ == "__main__":
    main()