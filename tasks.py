import json
import os
import time

from services import data_persistency
from services.repository import RepositoryService


repository_service = RepositoryService(
    organization=os.environ.get("GITHUB_ORGANIZATION"),
    api_token=os.environ.get("GITHUB_API_TOKEN"),
)


def retrieve_all_repositories_data_in_json_format():
    print("Retrieving all repositories...")
    repositories = repository_service.retrieve_all(repository_service.get_repositories)
    print(f"Retrieved {len(repositories)} repositories")

    with open("repositories.json", "w") as f:
        f.write(json.dumps(repositories, indent=2))

    for repository in repositories:
        ### Pull Requests ###
        print(f"Retrieving pull requests for {repository['name']}...")
        pull_requests = repository_service.retrieve_all(
            repository_service.get_repository_pull_requests,
            repository=repository["name"],
            state=repository_service.PullRequestStates.ALL,
        )
        print(f"Retrieved {len(pull_requests)} pull requests")

        with open(f"pull_requests/{repository['name']}.json", "w") as f:
            f.write(json.dumps(pull_requests, indent=2))

        ### Commits ###
        print("Retrieving all commits...")
        commits = repository_service.retrieve_all(
            repository_service.get_repository_commits, repository=repository["name"]
        )
        print(f"Retrieved {len(commits)} commits")

        with open(f"commits/{repository['name']}.json", "w") as f:
            f.write(json.dumps(commits, indent=2))

        ### Review Comments ###
        print("Retrieving all review comments...")
        review_comments = repository_service.retrieve_all(
            repository_service.get_repository_review_comments,
            repository=repository["name"],
        )
        print(f"Retrieved {len(review_comments)} review comments")

        with open(f"review_comments/{repository['name']}.json", "w") as f:
            f.write(json.dumps(review_comments, indent=2))


def convert_all_json_into_csv():
    with open("repositories.json", "r") as f:
        repositories = json.loads(f.read())

    for repository in repositories:
        print(f"Converting {repository['name']} ...")
        try:
            start_time = time.time()
            data_persistency.convert_commits_json_into_csv(repository["name"])
            data_persistency.convert_pull_requests_json_into_csv(repository["name"])
            data_persistency.convert_review_comments_json_into_csv(repository["name"])
            print(
                f"Finished {repository['name']} in {time.time() - start_time} seconds"
            )
        except Exception as e:
            print(f"\n>>>>> Failed to convert {repository['name']}: {e}\n")


def merge_all_repositories_data():
    data_persistency.merge_all_repositories_commits_csvs()
    data_persistency.merge_all_repositories_pull_requests_csvs()
    data_persistency.merge_all_repositories_review_comments_csvs()


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
