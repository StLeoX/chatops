import openai
import socket

def is_openai_api_accessible(host="api.openai.com", port=443, timeout=3):
    """
    Check if the OpenAI API is accessible by trying to establish a socket connection.

    Parameters:
        host (str): Hostname of the API.
        port (int): Port number (default 443 for HTTPS).
        timeout (int): Connection timeout in seconds.

    Returns:
        bool: True if the API is accessible, False otherwise.
    """
    try:
        # Create a socket object
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        # OSError is raised upon connection failure
        return False


def validate_api_key(key):
    """
    Validate the given API key.

    Parameters:
        key (str): The API key to be validated.

    Returns:
        bool: True if the API key is valid, False otherwise.
    """
    # Check openai is accessible
    if not is_openai_api_accessible():
        print("OpenAI API is not accessible.")
        return False

    openai.api_key = key
    try:
        openai.Model.list()
    except openai.error.AuthenticationError as e:
        return False
    else:
        return True