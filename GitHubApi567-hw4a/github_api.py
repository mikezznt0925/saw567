import requests


def get_user_repos_with_commit_counts(user_id):
    repos = _fetch_repos(user_id)
    if not repos:
        return []

    result = []
    for repo_info in repos:
        name = repo_info.get("name")
        if not name:
            continue
        commits = _fetch_commit_count(user_id, name)
        result.append({"repo": name, "commits": commits})
    return result


def _fetch_repos(user_id):
    url = f"https://api.github.com/users/{user_id}/repos"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except (requests.RequestException, ValueError):
        return []


def _fetch_commit_count(user_id, repo_name):
    url = f"https://api.github.com/repos/{user_id}/{repo_name}/commits"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return len(data) if isinstance(data, list) else 0
    except (requests.RequestException, ValueError):
        return 0


def format_repos_output(repos_with_commits):
    return [
        f"Repo: {item['repo']} Number of commits: {item['commits']}"
        for item in repos_with_commits
    ]


def run(user_id):
    data = get_user_repos_with_commit_counts(user_id)
    lines = format_repos_output(data)
    for line in lines:
        print(line)
    return lines


if __name__ == "__main__":
    import sys
    user = sys.argv[1] if len(sys.argv) > 1 else "richkempinski"
    run(user)
