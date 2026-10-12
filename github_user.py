import requests


def get_public_repos_count(username):
    response = requests.get(f"https://api.github.com/users/{username}", timeout=10)
    if response.status_code == 404:
        raise ValueError(f"User {username} not found")
    response.raise_for_status()
    return response.json()["public_repos"]


if __name__ == "__main__":
    print(get_public_repos_count("vsayyan"))