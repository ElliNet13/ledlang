import subprocess
import os

def run_git_command(cmd):
    return subprocess.check_output(cmd, text=True).strip()

# --- Git data ---
# Get current commit ID
commit_id = run_git_command(["git", "rev-parse", "HEAD"])

# Define your repo URL here
github_repo = "https://github.com/ElliNet13/ledlang"
commit_link = f"{github_repo}/commit/{commit_id}"

def get_current_tag():
    # Try to get the tag of the current commit
    try:
        tag = run_git_command(["git", "describe", "--exact-match", "--tags", "HEAD"])
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
}

# --- Replace in README.md ---
with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

for key, value in replacements.items():
    content = content.replace(f"{{{{{key}}}}}", value)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(content)

print("README.md updated with Git commit info and custom fillers.")
