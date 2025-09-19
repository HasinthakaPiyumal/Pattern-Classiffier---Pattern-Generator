import json
import os
import subprocess

json_file = "/home/hasinthaka/Documents/Projects/AI/AI Pattern Mining/Pattern Validator/data/mined_repo_urls/repositories_basic_queries_20250910-103728.json"

clone_dir = "/home/hasinthaka/Documents/Projects/AI/AI Pattern Mining/Pattern Validator/reposistories/mined_repos"
os.makedirs(clone_dir, exist_ok=True)

with open(json_file, "r") as f:
    repo_list = json.load(f)

for repo in repo_list:
    git_url = repo.get("svn_url")
    if git_url:
        repo_name = git_url.split("/")[-1]
        dest_path = os.path.join(clone_dir, repo_name)
        if not os.path.exists(dest_path):
            print(f"Cloning {git_url} into {dest_path} ...")
            subprocess.run(["git", "clone", git_url, dest_path])
        else:
            print(f"{repo_name} already exists in {clone_dir}, skipping.")
