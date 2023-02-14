accepted_api_errors = {
    403: [
        "Dependabot alerts are not available for archived repositories.",
        "Dependabot alerts are disabled for this repository.",
        "Resource not accessible by personal access token",
    ]
}


def exception_handler(response):
    if response.status_code in accepted_api_errors.keys():
        error_message = response.json().get("message")
        if error_message in accepted_api_errors[response.status_code]:
            return True, error_message

    return False, Exception(
        f"{response.status_code} {response.reason}: {response.text}"
    )
