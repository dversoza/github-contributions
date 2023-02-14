import json
import os

from services import data_persistency
from services.repository import RepositoryService


repository_service = RepositoryService(
    organization=os.environ.get("GITHUB_ORGANIZATION"),
    api_token=os.environ.get("GITHUB_API_TOKEN"),
)


def _retrieve_commits_for_repository(repository_name):
    print(f"Retrieving commits for {repository_name}...")
    commits = repository_service.retrieve_all(
        repository_service.get_repository_commits, repository=repository_name
    )
    print(f"Retrieved {len(commits)} commits")

    with open(f"commits/{repository_name}.json", "w") as f:
        f.write(json.dumps(commits, indent=2))


def _retrieve_dependabot_alerts_for_repository(repository_name):
    print(f"Retrieving dependabot alerts for {repository_name}...")
    dependabot_alerts = repository_service.retrieve_all(
        repository_service.get_repository_dependabot_alerts, repository=repository_name
    )
    print(f"Retrieved {len(dependabot_alerts)} dependabot alerts")

    with open(f"dependabot_alerts/{repository_name}.json", "w") as f:
        f.write(json.dumps(dependabot_alerts, indent=2))

    data_persistency.convert_dependabot_alerts_json_into_csv(repository_name)


def _retrieve_pull_requests_for_repository(repository_name):
    print(f"Retrieving pull requests for {repository_name}...")
    pull_requests = repository_service.retrieve_all(
        repository_service.get_repository_pull_requests,
        repository=repository_name,
        state=repository_service.PullRequestStates.ALL,
    )
    print(f"Retrieved {len(pull_requests)} pull requests")

    with open(f"pull_requests/{repository_name}.json", "w") as f:
        f.write(json.dumps(pull_requests, indent=2))


def _retrieve_review_comments_for_repository(repository_name):
    print(f"Retrieving review comments for {repository_name}...")
    review_comments = repository_service.retrieve_all(
        repository_service.get_repository_review_comments, repository=repository_name
    )
    print(f"Retrieved {len(review_comments)} review comments")

    with open(f"review_comments/{repository_name}.json", "w") as f:
        f.write(json.dumps(review_comments, indent=2))


def retrieve_all_repositories_data():
    repositories = repository_service.update_repositories_json_file()

    for repository in repositories:
        ### Commits ###
        _retrieve_commits_for_repository(repository["name"])

        ### Dependabot Alerts ###
        _retrieve_dependabot_alerts_for_repository(repository["name"])

        ### Pull Requests ###
        _retrieve_pull_requests_for_repository(repository["name"])

        ### Review Comments ###
        _retrieve_review_comments_for_repository(repository["name"])

    data_persistency.merge_all_repositories_commits_csvs()
    data_persistency.merge_all_repositories_dependabot_alerts_csvs()
    data_persistency.merge_all_repositories_pull_requests_csvs()
    data_persistency.merge_all_repositories_review_comments_csvs()


def retrieve_all_commits():
    repositories = repository_service.update_repositories_json_file()

    for repository in repositories:
        _retrieve_commits_for_repository(repository["name"])

    data_persistency.merge_all_repositories_commits_csvs()


def retrieve_all_dependabot_alerts():
    repositories = repository_service.update_repositories_json_file()

    for repository in repositories:
        _retrieve_dependabot_alerts_for_repository(repository["name"])

    data_persistency.merge_all_repositories_dependabot_alerts_csvs()


def retrieve_all_pull_requests():
    repositories = repository_service.update_repositories_json_file()

    for repository in repositories:
        _retrieve_pull_requests_for_repository(repository["name"])

    data_persistency.merge_all_repositories_pull_requests_csvs()


def retrieve_all_review_comments():
    repositories = repository_service.update_repositories_json_file()

    for repository in repositories:
        _retrieve_review_comments_for_repository(repository["name"])

    data_persistency.merge_all_repositories_review_comments_csvs()


TASKS = [
    ("Retrieve all repositories Commits", retrieve_all_commits),
    ("Retrieve all repositories Dependabot Alerts", retrieve_all_dependabot_alerts),
    ("Retrieve all repositories Pull Requests", retrieve_all_pull_requests),
    ("Retrieve all repositories Review Comments", retrieve_all_review_comments),
    ("Retrieve all data from all repositories", retrieve_all_repositories_data),
]
