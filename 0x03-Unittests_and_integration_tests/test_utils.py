#!/usr/bin/env python3
"""Unit tests for utils.py"""

import unittest
from unittest.mock import patch
from parameterized import parameterized


from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Tests the access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map returns expected output."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test access_nested_map raises KeyError."""
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Tests the get_json function."""

    @patch('utils.requests.get')
    def test_get_json(self, mock_get):
        """Test that get_json returns expected JSON payload."""
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
            result_1 = test.a_property
            result_2 = test.a_property

            self.assertEqual(result_1, 42)
            self.assertEqual(result_2, 42)
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
