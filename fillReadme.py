import subprocess
import os

def run_git_command(cmd):
    return subprocess.check_output(cmd, text=True).strip()

# --- Git data ---
# Get current commit ID
commit_id = run_git_command(["git", "rev-parse", "HEAD"])

owner = "ElliNet13"
repo = "ledlang"

# Define your repo URL here
github_repo = f"https://github.com/{owner}/{repo}"
commit_link = f"{github_repo}/commit/{commit_id}"

import requests

def get_latest_job_id(owner, repo, workflow_filename, token):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
    }

    # Step 1: Get latest workflow run ID
    runs_url = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow_filename}/runs?per_page=1"
    runs_resp = requests.get(runs_url, headers=headers)
    runs_resp.raise_for_status()
    runs_data = runs_resp.json()

    if not runs_data.get("workflow_runs"):
        raise Exception("No workflow runs found.")

    latest_run_id = runs_data["workflow_runs"][0]["id"]

    # Step 2: Get jobs for that workflow run
    jobs_url = f"https://api.github.com/repos/{owner}/{repo}/actions/runs/{latest_run_id}/jobs"
    jobs_resp = requests.get(jobs_url, headers=headers)
    jobs_resp.raise_for_status()
    jobs_data = jobs_resp.json()

    if not jobs_data.get("jobs"):
        raise Exception("No jobs found in the latest workflow run.")

    # Assuming single job in the run
    latest_job_id = jobs_data["jobs"][0]["id"]
    return latest_job_id

def get_current_tag():
    # Try to get the tag of the current commit
    try:
        tag = run_git_command(["git", "describe", "--tags", "HEAD"])
        return tag
    except subprocess.CalledProcessError:
        return None

def get_previous_tag(current_tag):
    # Get previous tag sorted by version/date before current_tag
    try:
        # List all tags reachable from HEAD, sorted by version (descending)
        tags = run_git_command(["git", "tag", "--sort=-creatordate"]).splitlines()
        # Find the current tag's position
        if current_tag in tags:
            current_index = tags.index(current_tag)
            # Return the next tag after current_tag in sorted list (previous version)
            if current_index + 1 < len(tags):
                return tags[current_index + 1]
        return None
    except Exception:
        return None

current_tag = get_current_tag()

if current_tag:
    previous_tag = get_previous_tag(current_tag)
    if previous_tag:
        # Get commits between previous_tag and current_tag (new version)
        commit_log = run_git_command([
            "git", "log", f"{previous_tag}..{current_tag}",
            "--pretty=format:- [%h](" + github_repo + "/commit/%H): %s"
        ])
    else:
        # No previous tag found, list commits up to current_tag
        commit_log = run_git_command([
            "git", "log", f"{current_tag}",
            "--pretty=format:- [%h](" + github_repo + "/commit/%H): %s"
        ])
else:
    # Not a tagged commit: fallback to previous commit comparison
    try:
        previous = run_git_command(["git", "rev-parse", "HEAD^"])
        commit_log = run_git_command([
            "git", "log", f"{previous}..HEAD",
            "--pretty=format:- [%h](" + github_repo + "/commit/%H): %s"
        ])
    except subprocess.CalledProcessError:
        commit_log = run_git_command([
            "git", "log", "HEAD", "-1",
            "--pretty=format:- [%h](" + github_repo + "/commit/%H): %s"
        ])

# --- Fillers to replace ---
replacements = {
    "markdownFormattedListOfCommits": commit_log,
    "githubRepoLink": github_repo,
   "badgeForTests": (
        f"![Test Status Badge](https://img.shields.io/badge/dynamic/json?"
        f"url=https%3A%2F%2Fapi.github.com%2Frepos%2FElliNet13%2Fledlang%2Factions%2Fjobs%2F"
        f"{get_latest_job_id(owner, repo, 'pytest.yml', os.environ['GITHUB_TOKEN'])}"
        f"&query=status&logo=github&label=Test%20Status)"
    )
}

# --- Replace in README.md ---
with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

for key, value in replacements.items():
    content = content.replace(f"{{{{{key}}}}}", value)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(content)

print("README.md updated with Git commit info and custom fillers.")
