import os
import requests
from yaml import safe_load

headers = {
    "Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
    "Accept": "application/vnd.github.v3+json",
}
config = requests.get("https://raw.githubusercontent.com/pulp/pulpcore/main/template_config.yml").content
branches = safe_load(config)["ci_update_branches"]

github_api = "https://api.github.com"

for branch in branches:
    print(f"Updating {branch}")
    if type(branch) == float and branch < 3.22 :
        workflow_path = "/actions/workflows/publish_images.yaml/dispatches"
    else:
        workflow_path = "/actions/workflows/pulp_images.yml/dispatches"
    url = f"{github_api}/repos/pulp/pulp-oci-images{workflow_path}"
    requests.post(url, headers=headers, json={"ref": branch})
