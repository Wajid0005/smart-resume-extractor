from http.client import responses

import requests
import base64

def get_github_profile(username):
    url = f"https://api.github.com/users/{username}"

    response = requests.get(url)

    return response.json()

def get_user_repositories(username):
    url = f"https://api.github.com/users/{username}/repos?per_page=100&sort=updated"

    response = requests.get(url)

    return response.json()

def clean_profile_data(profile):

    return {
        "name": profile.get("name"),
        "bio": profile.get("bio"),
        "location": profile.get("location"),
        "followers": profile.get("followers"),
        "public_repos": profile.get("public_repos"),
        "github_url": profile.get("html_url")

    }

def get_readme(owner, repo_name):
    url = f"https://api.github.com/repos/{owner}/{repo_name}/readme"

    response = requests.get(url)

    if response.status_code != 200:
        return "README file not found"

    data = response.json()
    content = base64.b64decode(data["content"]).decode("utf-8")

    return content