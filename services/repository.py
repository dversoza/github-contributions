import json
from enum import Enum
from typing import List

from .base import BaseGithubAPIService


class RepositoryService(BaseGithubAPIService):
    class PullRequestStates(Enum):
        OPEN = "open"
        CLOSED = "closed"
        ALL = "all"

    def __init__(self, organization: str, api_token: str, *args, **kwargs) -> None:
        super().__init__(organization, api_token, *args, **kwargs)

    def get_repositories(
        self, page: int = 1, per_page: int = 30, *args, **kwargs
    ) -> List[dict]:
        url = f"{self.GITHUB_API_BASE_URL}/orgs/{self.organization}/repos"

        return self.base_request(
            self.AllowedMethods.GET, url, page=page, per_page=per_page, *args, **kwargs
        )

    def get_repository_commits(
        self, repository: str, page: int = 1, per_page: int = 30, *args, **kwargs
    ) -> list:
        url = (
            f"{self.GITHUB_API_BASE_URL}/repos/{self.organization}/{repository}/commits"
        )

        return self.base_request(
            self.AllowedMethods.GET, url, page=page, per_page=per_page, *args, **kwargs
        )

    def get_repository_pull_requests(
        self,
        repository: str,
        page: int = 1,
        per_page: int = 30,
        state: PullRequestStates = PullRequestStates.OPEN,
        *args,
        **kwargs,
    ) -> list:
        url = f"{self.GITHUB_API_BASE_URL}/repos/{self.organization}/{repository}/pulls"

        params = {
            "state": state.value,
            "page": page,
            "per_page": per_page,
        }

        return self.base_request(
            self.AllowedMethods.GET, url, params=params, *args, **kwargs
        )

    def get_repository_review_comments(
        self, repository: str, page: int = 1, per_page: int = 30, *args, **kwargs
    ) -> list:
        url = f"{self.GITHUB_API_BASE_URL}/repos/{self.organization}/{repository}/pulls/comments"

        return self.base_request(
            self.AllowedMethods.GET, url, page=page, per_page=per_page, *args, **kwargs
        )

    def get_repository_dependabot_alerts(
        self, repository: str, page: int = 1, per_page: int = 30, *args, **kwargs
    ) -> list:
        url = f"{self.GITHUB_API_BASE_URL}/repos/{self.organization}/{repository}/dependabot/alerts"

        return self.base_request(
            self.AllowedMethods.GET, url, page=page, per_page=per_page, *args, **kwargs
        )

    def update_repositories_json_file(self) -> List[dict]:
        print("Updating repositories file...")
        repositories = self.retrieve_all(self.get_repositories)
        print(f"Retrieved {len(repositories)} repositories")

        with open("repositories.json", "w") as f:
            f.write(json.dumps(repositories, indent=2))

        return repositories
