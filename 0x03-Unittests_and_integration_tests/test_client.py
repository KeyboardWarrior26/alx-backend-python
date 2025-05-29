#!/usr/bin/env python3
"""Unit and Integration tests for client.py module."""

import unittest
from unittest.mock import patch, MagicMock, PropertyMock
from parameterized import parameterized

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test GithubOrgClient class"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test org method returns correct output."""
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, test_payload)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """Test _public_repos_url returns correct URL."""
        with patch.object(GithubOrgClient, 'org',
                          new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {
                'repos_url': "http://test.com/orgs/google/repos"
            }

            client = GithubOrgClient("google")
            self.assertEqual(client._public_repos_url,
                             "http://test.com/orgs/google/repos")

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns correct list."""
        payload = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = payload

        with patch.object(GithubOrgClient, '_public_repos_url',
                          new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "http://test.com/orgs/google/repos"

            client = GithubOrgClient("google")
            self.assertEqual(client.public_repos(), ["repo1", "repo2"])
            mock_get_json.assert_called_once_with(
                "http://test.com/orgs/google/repos"
            )

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns correct boolean."""
        self.assertEqual(GithubOrgClient.has_license(repo, license_key),
                         expected)


@patch('client.get_json')
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for GithubOrgClient.public_repos method"""

    @classmethod
    def setUpClass(cls):
        """Set up test payloads"""
        cls.org_payload = {
            "repos_url": "http://test.com/orgs/google/repos"
        }
        cls.repos_payload = [
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "mit"}},
            {"name": "repo3", "license": {"key": "apache-2.0"}}
        ]

    def test_public_repos(self, mock_get_json):
        """Test public_repos returns all repos"""
        mock_get_json.side_effect = [
            self.org_payload,
            self.repos_payload
        ]
        client = GithubOrgClient("google")
        result = client.public_repos()
        self.assertEqual(result, ["repo1", "repo2", "repo3"])

    def test_public_repos_with_license(self, mock_get_json):
        """Test public_repos returns only Apache 2.0 licensed repos"""
        mock_get_json.side_effect = [
            self.org_payload,
            self.repos_payload
        ]
        client = GithubOrgClient("google")
        result = client.public_repos(license="apache-2.0")
        self.assertEqual(result, ["repo1", "repo3"])
