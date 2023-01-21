# Github Analytics Data Retriever

This is a simple script to retrieve data from the Github API.
It is designed to retrieve data from an organization repositories and store it in a CSV file.

## Requirements

### Interpreter

* Python 3.7+

### Libraries

* [Requests](https://pypi.org/project/requests/)
* [Pandas](https://pypi.org/project/pandas/)
* [python-dotenv](https://pypi.org/project/python-dotenv/)

### Github API Token

You need to create a Github API token to use this script. You can do it by following the instructions [here](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token).

## Usage

### Configuration

You need to create a `.env` file in the root directory of the project. This file will contain the following variables:

* `GITHUB_API_TOKEN`: Your Github API token.
* `GITHUB_ORGANIZATION`: The name of the organization you want to retrieve data from.

### Installation

1. Clone this repository.
2. Create a virtual environment by running the following command:

    ```bash
    python3 -m venv venv
    ```

3. Activate the virtual environment by running the following command:

    ```bash
    source venv/bin/activate
    ```

4. Install the dependencies by running the following command:

    ```bash
    pip install -r requirements.txt
    ```

### Execution

With your virtual environment enabled, you can execute the script by running the following command:

```bash
python main.py
```

The script will create `.json` and `.csv` files with the extracted data in the root directory of the project.

## Available data

The following data is available:

* All Repository data
* Repository **Commits** data
* Repository **Pull Requests** data
* Repository **Review Comments** data

# TODOs

## [#1 PRIORITY] Display the following counts in a dashboard

[ ] Total number of commits per user
[ ] Total number of open pull requests per user
[ ] Total number of comments per user
[ ] Total number of reviews in pull requests per user

## [#2 PRIORITY] Display the following counts in a dashboard

[ ] Total number of comments in pull requests per user
[ ] Total number of merged pull requests per user
[ ] Total number of comments in issues per user
[ ] Total number of closed pull requests per user
[ ] Total number of open issues per user
