import json
import os
import time
from enum import Enum
from typing import List

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_API_BASE_URL = "https://api.github.com"
GITHUB_API_TOKEN = os.environ.get("GITHUB_API_TOKEN")
GITHUB_ORGANIZATION = os.environ.get("GITHUB_ORGANIZATION")


class AllowedMethods(Enum):
    GET = "GET"
    POST = "POST"


class PullRequestStates(Enum):
    OPEN = "open"
    CLOSED = "closed"
    ALL = "all"


def base_request(
    method: AllowedMethods, url: str, *args, **kwargs
) -> List[dict] | dict:
    headers = {
        "Authorization": f"Bearer {GITHUB_API_TOKEN}",
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
        raise Exception(f"{response.status_code} {response.reason}: {response.text}")

    return response.json()


def get_repositories(page: int = 1, per_page: int = 30, *args, **kwargs) -> List[dict]:
    url = f"{GITHUB_API_BASE_URL}/orgs/{GITHUB_ORGANIZATION}/repos"

    return base_request(
        AllowedMethods.GET, url, page=page, per_page=per_page, *args, **kwargs
    )


def get_repository_commits(
    repository: str, page: int = 1, per_page: int = 30, *args, **kwargs
) -> list:
    url = f"{GITHUB_API_BASE_URL}/repos/{GITHUB_ORGANIZATION}/{repository}/commits"

    return base_request(
        AllowedMethods.GET, url, page=page, per_page=per_page, *args, **kwargs
    )


def get_repository_pull_requests(
    repository: str,
    page: int = 1,
    per_page: int = 30,
    state: PullRequestStates = PullRequestStates.OPEN,
    *args,
    **kwargs,
) -> list:
    url = f"{GITHUB_API_BASE_URL}/repos/{GITHUB_ORGANIZATION}/{repository}/pulls"

    params = {
        "state": state.value,
        "page": page,
        "per_page": per_page,
    }

    return base_request(AllowedMethods.GET, url, params=params, *args, **kwargs)


def get_repository_review_comments(
    repository: str, page: int = 1, per_page: int = 30, *args, **kwargs
) -> list:
    url = (
        f"{GITHUB_API_BASE_URL}/repos/{GITHUB_ORGANIZATION}/{repository}/pulls/comments"
    )

    return base_request(
        AllowedMethods.GET, url, page=page, per_page=per_page, *args, **kwargs
    )


def retrieve_all(method, *args, **kwargs):
    page = 1 or kwargs.get("page")
    per_page = 100 or kwargs.get("per_page")

    response = method(page=page, per_page=per_page, *args, **kwargs)
    all_results = response

    while len(response) == per_page:
        page += 1
        response = method(page=page, per_page=per_page, *args, **kwargs)

        all_results.extend(response)

    return all_results


def retrieve_all_repositories_data_in_json_format():
    print("Retrieving all repositories...")
    repositories = retrieve_all(get_repositories)
    print(f"Retrieved {len(repositories)} repositories")

    with open("repositories.json", "w") as f:
        f.write(json.dumps(repositories, indent=2))

    for repository in repositories:
        ### Pull Requests ###
        print(f"Retrieving pull requests for {repository['name']}...")
        pull_requests = retrieve_all(
            get_repository_pull_requests,
            repository=repository["name"],
            state=PullRequestStates.ALL,
        )
        print(f"Retrieved {len(pull_requests)} pull requests")

        with open(f"pull_requests/{repository['name']}.json", "w") as f:
            f.write(json.dumps(pull_requests, indent=2))

        ### Commits ###
        print("Retrieving all commits...")
        commits = retrieve_all(get_repository_commits, repository=repository["name"])
        print(f"Retrieved {len(commits)} commits")

        with open(f"commits/{repository['name']}.json", "w") as f:
            f.write(json.dumps(commits, indent=2))

        ### Review Comments ###
        print("Retrieving all review comments...")
        review_comments = retrieve_all(
            get_repository_review_comments, repository=repository["name"]
        )
        print(f"Retrieved {len(review_comments)} review comments")

        with open(f"review_comments/{repository['name']}.json", "w") as f:
            f.write(json.dumps(review_comments, indent=2))


def convert_commits_json_into_csv(repository: str):
    df = pd.read_json(f"commits/{repository}.json")

    if df.empty:
        print(f"Repository {repository} has no commits")
        return

    df = df[["sha", "commit", "author", "committer"]]

    df["message"] = df["commit"].apply(lambda x: x["message"] if x else None)
    df["date"] = df["commit"].apply(lambda x: x["author"]["date"] if x else None)
    df["author"] = df["author"].apply(lambda x: x["login"] if x else None)
    df["committer"] = df["committer"].apply(lambda x: x["login"] if x else None)

    df = df[["sha", "message", "date", "author", "committer"]]

    df.to_csv(f"commits/{repository}.csv", index=False)


def convert_pull_requests_json_into_csv(repository: str):
    df = pd.read_json(f"pull_requests/{repository}.json")

    if df.empty:
        print(f"Repository {repository} has no commits")
        return

    df = df[
        [
            "id",
            "number",
            "title",
            "state",
            "created_at",
            "updated_at",
            "closed_at",
            "merged_at",
            "user",
            "assignee",
            "requested_reviewers",
        ]
    ]

    df["user"] = df["user"].apply(lambda x: x["login"] if x else None)
    df["assignee"] = df["assignee"].apply(lambda x: x["login"] if x else None)
    df["requested_reviewers"] = df["requested_reviewers"].apply(
        lambda x: [y["login"] for y in x] if x else None
    )

    df.to_csv(f"pull_requests/{repository}.csv", index=False)


def convert_review_comments_json_into_csv(repository: str):
    df = pd.read_json(f"review_comments/{repository}.json")

    if df.empty:
        print(f"Repository {repository} has no commits")
        return

    df = df[["id", "user", "body", "created_at", "updated_at"]]

    df["user"] = df["user"].apply(lambda x: x["login"] if x else None)

    df.to_csv(f"review_comments/{repository}.csv", index=False)


def convert_all_json_into_csv():
    with open("repositories.json", "r") as f:
        repositories = json.loads(f.read())

    for repository in repositories:
        print(f"Converting {repository['name']} ...")
        try:
            start_time = time.time()
            convert_commits_json_into_csv(repository["name"])
            convert_pull_requests_json_into_csv(repository["name"])
            convert_review_comments_json_into_csv(repository["name"])
            print(
                f"Finished {repository['name']} in {time.time() - start_time} seconds"
            )
        except Exception as e:
            print(f"\n>>>>> Failed to convert {repository['name']}: {e}\n")


def merge_all_repositories_commits():
    with open("repositories.json", "r") as f:
        repositories = json.loads(f.read())

    df = pd.DataFrame()

    for repository in repositories:
        if os.path.exists(f"commits/{repository['name']}.csv"):
            commits = pd.read_csv(f"commits/{repository['name']}.csv")
            commits["repository"] = repository["name"]
            df = pd.concat([df, commits])

    df.to_csv("commits.csv", index=False)


def merge_all_repositories_pull_requests():
    with open("repositories.json", "r") as f:
        repositories = json.loads(f.read())

    df = pd.DataFrame()

    for repository in repositories:
        if os.path.exists(f"pull_requests/{repository['name']}.csv"):
            pull_requests = pd.read_csv(f"pull_requests/{repository['name']}.csv")
            pull_requests["repository"] = repository["name"]
            df = pd.concat([df, pull_requests])

    df.to_csv("pull_requests.csv", index=False)


def merge_all_repositories_review_comments():
    with open("repositories.json", "r") as f:
        repositories = json.loads(f.read())

    df = pd.DataFrame()

    for repository in repositories:
        if os.path.exists(f"review_comments/{repository['name']}.csv"):
            review_comments = pd.read_csv(f"review_comments/{repository['name']}.csv")
            review_comments["repository"] = repository["name"]
            df = pd.concat([df, review_comments])

    df.to_csv("review_comments.csv", index=False)


def merge_all_repositories_data():
    merge_all_repositories_commits()
    merge_all_repositories_pull_requests()
    merge_all_repositories_review_comments()


def main():
    TASKS = [
        (
            "Retrieve repositories analytics data from Github (commits, pull requests and review comments)",
            retrieve_all_repositories_data_in_json_format,
        ),
        ("Convert all JSON files into CSV files", convert_all_json_into_csv),
        (
            "Merge all repositories data into one CSV file (to analyze in Excel or similar)",
            merge_all_repositories_data,
        ),
    ]
    print("\n=====================================================")
    print("Github Analytics Data Retriever")
    print("=====================================================")
    print("\nWelcome! What do you want to do?\n")

    for idx, task in enumerate(TASKS):
        print(f"\t{idx + 1} - {task[0]}")

    task = int(input("\nPlease enter the number of the task you want to execute: "))

    if task < 1 or task > len(TASKS):
        print("Invalid task number")
        return

    print(f"\nExecuting task \#{task} - {TASKS[task - 1][0]} ...\n")
    time.sleep(1)
    start_time = time.time()
    TASKS[task - 1][1]()
    print(f"\nFinished {TASKS[task - 1][0]} in {time.time() - start_time} seconds")

    print("\n=====================================================")
    print("Thank you for using Github Analytics Data Retriever!")
    print("=====================================================")


if __name__ == "__main__":
    main()
