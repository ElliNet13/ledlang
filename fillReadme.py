import subprocess
import os

def run_git_command(cmd):
    return subprocess.check_output(cmd, text=True).strip()

# --- Git data ---
# Get latest commit ID
commit_id = run_git_command(["git", "rev-parse", "HEAD"])

# Define your repo URL here
github_repo = "https://github.com/ElliNet13/ledlang"
commit_link = f"{github_repo}/commit/{commit_id}"

# Try to get the previous commit (HEAD^)
try:
    previous = run_git_command(["git", "rev-parse", "HEAD^"])
except subprocess.CalledProcessError:
    previous = None

# Get markdown list of commits
if previous:
    commit_log = run_git_command([
        "git", "log", f"{previous}..HEAD",
        "--pretty=format:- [%h](" + github_repo + "/commit/%H): %s"
    ])
else:
    commit_log = run_git_command([
        "git", "log", "HEAD", "-1",
        "--pretty=format:- [%h](" + github_repo + "/commit/%H): %s"
    ])

# --- Fillers to replace ---
replacements = {
    "markdownFormattedListOfCommits": commit_log,
    "githubRepoLink": github_repo,
    "testStatus": os.getenv("PREV_WORKFLOW_CONCLUSION")
}

# --- Replace in README.md ---
with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

for key, value in replacements.items():
    content = content.replace(f"{{{{{key}}}}}", value)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(content)

print("README.md updated with Git commit info and custom fillers.")
