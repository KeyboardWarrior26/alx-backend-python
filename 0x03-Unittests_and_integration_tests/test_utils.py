#!/usr/bin/env python3
"""Unit tests for utils.py"""

import unittest
from parameterized import parameterized
from unittest.mock import patch
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for access_nested_map."""

    def test_access_nested_map(self):
        """Test correct access to values in a nested map."""
        nested_map = {"a": {"b": 2}}
        self.assertEqual(access_nested_map(nested_map, ("a",)), {"b": 2})
        self.assertEqual(access_nested_map(nested_map, ("a", "b")), 2)

    def test_access_nested_map_exception(self):
        """Test KeyError is raised for missing keys."""
        nested_map = {"a": 1}
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, ("a", "b"))


class TestGetJson(unittest.TestCase):
    """Test cases for get_json."""

    @patch('utils.requests.get')
    def test_get_json(self, mock_get):
        """Test that get_json returns the expected payload."""
        test_url = "http://example.com"
        test_payload = {"payload": True}
        mock_get.return_value.json.return_value = test_payload

        result = get_json(test_url)
        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Tests for the memoize decorator."""

    def test_memoize(self):
        """Test that memoize caches the result of the method call."""
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(
            TestClass,
            'a_method',
            return_value=42
        ) as mock_method:
            test = TestClass()
            result_1 = test.a_property()
            result_2 = test.a_property()

            self.assertEqual(result_1, 42)
            self.assertEqual(result_2, 42)
            mock_method.assert_called_once()
