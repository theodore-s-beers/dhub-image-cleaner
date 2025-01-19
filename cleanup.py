import os
import time
from typing import Any

import requests
from dotenv import load_dotenv

USERNAME = "katomyomachia"
REPOSITORY = "engr-131-api"

TAGS_URL = f"https://hub.docker.com/v2/repositories/{USERNAME}/{REPOSITORY}/tags"


# Fetch all tags for the repository
def fetch_tags(token: str, pause: float = 1.0) -> list[dict[str, Any]]:
    tags: list[dict[str, Any]] = []
    page: int = 1

    while True:
        response = requests.get(
            TAGS_URL,
            headers={"Authorization": f"Bearer {token}"},
            params={"page_size": 100, "page": page},
        )
        response.raise_for_status()

        data = response.json()
        tags.extend(data["results"])

        if not data["next"]:
            break

        page += 1
        time.sleep(pause)

    return tags


# Delete a tag by name
def delete_tag(token: str, tag_name: str) -> None:
    delete_url = f"{TAGS_URL}/{tag_name}"
    response = requests.delete(delete_url, headers={"Authorization": f"Bearer {token}"})
    response.raise_for_status()
    print(f"Deleted tag: {tag_name}")


# Main function
def cleanup_old_tags(pause: float = 1.0) -> None:
    load_dotenv()

    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    if not ACCESS_TOKEN:
        raise ValueError("ACCESS_TOKEN environment variable not set")

    tags = fetch_tags(ACCESS_TOKEN)

    # Sort tags by last updated time (descending)
    tags.sort(key=lambda x: x["last_updated"], reverse=True)

    # Keep only the 10 most recent tags
    tags_to_delete = tags[10:]

    for tag in tags_to_delete:
        delete_tag(ACCESS_TOKEN, tag["name"])
        time.sleep(pause)

    print(f"Kept the 10 most recent tags; deleted {len(tags_to_delete)} old tags")


if __name__ == "__main__":
    cleanup_old_tags()
