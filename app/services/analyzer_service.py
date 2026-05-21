def extract_repo_data(repos):

    cleaned_data = []

    for repo in repos:

        cleaned_data.append({

            "name": repo.get("name"),

            "description": repo.get("description"),

            "language": repo.get("language"),

            "stars": repo.get("stargazers_count"),

            "forks": repo.get("forks_count")

        })

    return cleaned_data