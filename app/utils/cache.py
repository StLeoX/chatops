# Flask modules
from flask import current_app
from flask.wrappers import Request, Response

# Other modules
import logging

# Local modules
from app.extensions import cache


def make_api_cache_key(request: Request):
    """
    Generate a cache key for the API based on the request object.

    Parameters:
        request (Request): The request object containing the URL.

    Returns:
        str: The cache key for the API.
    """
    full_url = request.url
    api_cache_url = full_url.split("/v1/")[-1]
    return api_cache_url


def is_exempted_route(route_path: str):
    """
    Check if the given route path is exempted from caching.

    Parameters:
        route_path (str): The path of the route to be checked.

    Returns:
        bool: True if the route path is exempted from caching, False otherwise.
    """
    if any(
        route_path.startswith(x) for x in current_app.config["CACHE_EXEMPTED_ROUTES"]
    ):
        return True
    return False


def is_cachable(request: Request):
    """
    Check if a request is cachable.

    Parameters:
        request (Request): The request object.

    Returns:
        bool: True if the request is cachable, False otherwise.
    """
    if not current_app.config["CACHE_ENABLED"]:
        return False

    if is_exempted_route(request.path):
        return False

    return True


def get_cached_response(request: Request):
    """
    Returns a cached response.md if available for the given request, otherwise returns None.

    Parameters:
        request (Request): The request object for which to retrieve the cached response.md.

    Returns:
        Any: The cached response.md if available, otherwise None.

    Raises:
        Exception: If there is an error when fetching the cached response.md.
    """
    if not is_cachable(request):
        return None

    cache_key = make_api_cache_key(request)
    try:
        cached_response = cache.get(cache_key)
        if cached_response is not None:
            return cached_response
    except Exception as e:
        logging.error(f"Error when fetching cached response.md: {e}")

    return None


def set_cached_response(request: Request, response: Response):
    """
    Sets the cached response.md for the given request and response.md.

    Parameters:
        request (Request): The HTTP request object.
        response (Response): The HTTP response.md object.

    Returns:
        None
    """
    if not is_cachable(request):
        return None

    try:
        cache_key = make_api_cache_key(request)
        if not cache.get(cache_key):
            cache.set(cache_key, response)
    except Exception as e:
        logging.error(f"Error when caching response.md: {e}")

    return None
