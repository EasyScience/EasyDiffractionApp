__author__ = "github.com/wardsimon"
__version__ = "0.0.1"

import os
import requests
import yaml


repo = os.environ.get("GITHUB_REPOSITORY", "")
with open(os.environ.get("INPUT_CONFIG-FILE", ""), "r") as raw:
    cfg = yaml.safe_load(raw)
branches = cfg.get("branches", {})
access_token = os.environ.get("INPUT_GITHUB-TOKEN", "")

for branch in branches:
    r = requests.put(
        "https://api.github.com/repos/{0}/branches/{1}/protection".format(
            repo, branch.get("name", "")
        ),
        headers={
            "Accept": "application/vnd.github.luke-cage-preview+json",
            "Authorization": "Token {0}".format(access_token),
        },
        json=branch.get("protection", {}),
    )
    print(r.status_code)
    print(r.json())
