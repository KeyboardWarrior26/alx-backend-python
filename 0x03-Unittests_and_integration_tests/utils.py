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
    """Access nested map with key path."""
    for key in path:
        if not isinstance(nested_map, Mapping):
            raise KeyError(key)
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


def memoize(method):
    """Decorator that caches a method's output."""
    attr_name = "_{}".format(method.__name__)

    @property
    @wraps(method)
    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self))
        return getattr(self, attr_name)

    return wrapper
