from enum import Enum
from typing import List

import requests


class BaseGithubAPIService:
    GITHUB_API_BASE_URL = "https://api.github.com"

    class AllowedMethods(Enum):
        GET = "GET"
        POST = "POST"

    def __init__(self, organization: str, api_token: str) -> None:
        self.organization = organization
        self.api_token = api_token

    def base_request(
        self, method: AllowedMethods, url: str, *args, **kwargs
    ) -> List[dict] | dict:
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Accept": "application/vnd.github+json",  # Required for GitHub API v3
            "X-GitHub-Api-Version": "2022-11-28",  # Required for GitHub API v3
        } | kwargs.pop("headers", {})

        params = {
            "per_page": kwargs.pop("per_page", 30),
            "page": kwargs.pop("page", 1),
        } | kwargs.pop("params", {})

        response = requests.request(
            method.value, url, headers=headers, params=params, *args, **kwargs
        )

        if response.status_code != 200:
            raise Exception(
                f"{response.status_code} {response.reason}: {response.text}"
            )

        return response.json()

    def retrieve_all(self, method, *args, **kwargs):
        page = 1 or kwargs.get("page")
        per_page = 100 or kwargs.get("per_page")

        response = method(page=page, per_page=per_page, *args, **kwargs)
        all_results = response

        while len(response) == per_page:
            page += 1
            response = method(page=page, per_page=per_page, *args, **kwargs)

            all_results.extend(response)

        return all_results
