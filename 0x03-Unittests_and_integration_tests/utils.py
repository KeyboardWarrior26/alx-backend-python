#!/usr/bin/env python3
"""Generic utilities for github org client.
"""

import requests
from functools import wraps
from typing import (
    Mapping,
    Sequence,
    Any,
    Dict,
    Callable,
)


__all__ = [
    "access_nested_map",
    "get_json",
    "memoize",
]


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """Access a value in a nested map by following a sequence of keys.

    Args:
        nested_map (Mapping): A nested map.
        path (Sequence): A sequence of keys representing a path to the value.

    Returns:
        Any: The value located at the end of the path.
    """
    for key in path:
        nested_map = nested_map[key]
    return nested_map


def get_json(url: str) -> Dict:
    """Return the JSON content of a given URL.

    Args:
        url (str): The URL to fetch JSON from.

    Returns:
        Dict: The parsed JSON response.
    """
    response = requests.get(url)
    return response.json()


def memoize(method: Callable) -> Callable:
    """Decorator to memoize a method's return value.

    Args:
        method (Callable): The method to be memoized.

    Returns:
        Callable: The wrapped method with memoization.
    """
    attr_name = f"_memoized_{method.__name__}"

    @wraps(method)
    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self))
        return getattr(self, attr_name)

    return wrapper

