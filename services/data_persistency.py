import json
import os

import pandas as pd


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


def convert_dependabot_alerts_json_into_csv(repository: str):
    df = pd.read_json(f"dependabot_alerts/{repository}.json")

    if df.empty:
        print(f"Repository {repository} has no dependabot alerts")
        return

    df = df[
        [
            "number",
            "state",
            "dependency_name",
            "dependency_path",
            "cve_id",
            "summary",
            "description",
            "severity",
            "published_at",
            "updated_at",
            "vulnerable_package_name",
            "vulnerable_package_version",
            "first_patched_version",
            "url",
            "created_at",
        ]
    ]

    df["dependency_name"] = df["dependency_name"].apply(
        lambda x: x["dependency"]["package"]["name"] if x else None
    )
    df["dependency_path"] = df["dependency_path"].apply(
        lambda x: x["dependency"]["manifest_path"] if x else None
    )

    df["cve_id"] = df["cve_id"].apply(
        lambda x: x["security_advisory"]["cve_id"] if x else None
    )
    df["summary"] = df["summary"].apply(
        lambda x: x["security_advisory"]["summary"] if x else None
    )
    df["description"] = df["description"].apply(
        lambda x: x["security_advisory"]["description"] if x else None
    )
    df["severity"] = df["severity"].apply(
        lambda x: x["security_advisory"]["severity"] if x else None
    )
    df["published_at"] = df["published_at"].apply(
        lambda x: x["security_advisory"]["published_at"] if x else None
    )
    df["updated_at"] = df["updated_at"].apply(
        lambda x: x["security_advisory"]["updated_at"] if x else None
    )
    df["vulnerable_package_name"] = df["vulnerable_package_name"].apply(
        lambda x: x["security_advisory"]["vulnerabilities"][0]["package"]["name"]
        if x
        else None
    )
    df["vulnerable_package_version"] = df["vulnerable_package_version"].apply(
        lambda x: x["security_advisory"]["vulnerabilities"][0][
            "vulnerable_version_range"
        ]
        if x
        else None
    )
    df["first_patched_version"] = df["first_patched_version"].apply(
        lambda x: x["security_advisory"]["vulnerabilities"][0]["first_patched_version"][
            "identifier"
        ]
        if x
        else None
    )
    df["url"] = df["url"].apply(lambda x: x["html_url"] if x else None)
    df["created_at"] = df["created_at"].apply(lambda x: x["created_at"] if x else None)

    df.to_csv(f"dependabot_alerts/{repository}.csv", index=False)


def merge_all_repositories_commits_csvs():
    with open("repositories.json", "r") as f:
        repositories = json.loads(f.read())

    df = pd.DataFrame()

    for repository in repositories:
        if os.path.exists(f"commits/{repository['name']}.csv"):
            commits = pd.read_csv(f"commits/{repository['name']}.csv")
            commits["repository"] = repository["name"]
            df = pd.concat([df, commits])

    df.to_csv("commits.csv", index=False)


def merge_all_repositories_pull_requests_csvs():
    with open("repositories.json", "r") as f:
        repositories = json.loads(f.read())

    df = pd.DataFrame()

    for repository in repositories:
        if os.path.exists(f"pull_requests/{repository['name']}.csv"):
            pull_requests = pd.read_csv(f"pull_requests/{repository['name']}.csv")
            pull_requests["repository"] = repository["name"]
            df = pd.concat([df, pull_requests])

    df.to_csv("pull_requests.csv", index=False)


def merge_all_repositories_review_comments_csvs():
    with open("repositories.json", "r") as f:
        repositories = json.loads(f.read())

    df = pd.DataFrame()

    for repository in repositories:
        if os.path.exists(f"review_comments/{repository['name']}.csv"):
            review_comments = pd.read_csv(f"review_comments/{repository['name']}.csv")
            review_comments["repository"] = repository["name"]
            df = pd.concat([df, review_comments])

    df.to_csv("review_comments.csv", index=False)
