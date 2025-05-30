
import os
import requests

class SelfUpgradingTool:
    def __init__(self, version, repo_url):
        self.version = version
        self.repo_url = repo_url

    def check_for_updates(self):
        response = requests.get(self.repo_url)
        latest_version = response.json()['tag_name']

        if latest_version > self.version:
            print("New version available.")
            return True
        else:
            print("You are using the latest version.")
            return False

    def upgrade(self):
        if self.check_for_updates():
            os.system(f"pip install --upgrade {self.repo_url}")
            print("Upgrade successful.")
        else:
            print("No upgrade needed.")

if __name__ == "__main__":
    tool = SelfUpgradingTool('1.0.0', 'https://api.github.com/repos/username/repo/releases/latest')
    tool.upgrade()
