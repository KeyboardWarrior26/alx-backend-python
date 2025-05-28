#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient
from unittest.mock import patch, PropertyMock


class TestGithubOrgClient(unittest.TestCase):
    """Tests for the GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct value."""
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, test_payload)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")


def test_public_repos_url(self):
    """Test that _public_repos_url returns the correct URL."""
    with patch("client.GithubOrgClient.org", new_callable=PropertyMock) as mock_org:
        mock_org.return_value = {"repos_url": "https://api.github.com/orgs/google/repos"}

        client = GithubOrgClient("google")
        result = client._public_repos_url

        self.assertEqual(result, "https://api.github.com/orgs/google/repos")


@patch("client.get_json")
def test_public_repos(self, mock_get_json):
    """Test that public_repos returns expected list of repo names."""
    test_payload = [
        {"name": "repo1"},
        {"name": "repo2"},
        {"name": "repo3"},
    ]
    mock_get_json.return_value = test_payload

    with patch(
        "client.GithubOrgClient._public_repos_url",
        new_callable=PropertyMock
    ) as mock_repos_url:
        mock_repos_url.return_value = "https://api.github.com/orgs/google/repos"

        client = GithubOrgClient("google")
        result = client.public_repos()

        expected = ["repo1", "repo2", "repo3"]
        self.assertEqual(result, expected)

        mock_repos_url.assert_called_once()
        mock_get_json.assert_called_once_with("https://api.github.com/orgs/google/repos")
