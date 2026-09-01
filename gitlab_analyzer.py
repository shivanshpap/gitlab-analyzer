import os

from dotenv import load_dotenv


# Load variables from .env
load_dotenv()

GITLAB_URL = os.getenv("GITLAB_URL")
GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")


def main():
    if not GITLAB_URL:
        print("Error: GITLAB_URL is not set.")
        return

    if not GITLAB_TOKEN:
        print("Error: GITLAB_TOKEN is not set.")
        return

    print(f"GitLab URL: {GITLAB_URL}")
    print("GitLab token: [loaded successfully]")


if __name__ == "__main__":
    main()