import unittest
from unittest.mock import patch, Mock

import requests

from github_api import (
    get_user_repos_with_commit_counts,
    format_repos_output,
    run,
)


class TestFormatReposOutput(unittest.TestCase):

    def test_empty_list(self):
        self.assertEqual(format_repos_output([]), [])

    def test_single_repo(self):
        data = [{"repo": "Triangle567", "commits": 10}]
        self.assertEqual(
            format_repos_output(data),
            ["Repo: Triangle567 Number of commits: 10"],
        )

    def test_two_repos_as_in_spec(self):
        data = [
            {"repo": "Triangle567", "commits": 10},
            {"repo": "Square567", "commits": 27},
        ]
        self.assertEqual(
            format_repos_output(data),
            [
                "Repo: Triangle567 Number of commits: 10",
                "Repo: Square567 Number of commits: 27",
            ],
        )

    def test_zero_commits(self):
        data = [{"repo": "EmptyRepo", "commits": 0}]
        self.assertEqual(
            format_repos_output(data),
            ["Repo: EmptyRepo Number of commits: 0"],
        )


class TestGetUserReposWithCommitCounts(unittest.TestCase):

    @patch("github_api.requests.get")
    def test_returns_list_of_repo_and_commits(self, mock_get):
        mock_get.return_value.json.side_effect = [
            [{"name": "Triangle567"}, {"name": "Square567"}],
            [{}] * 10,
            [{}] * 27,
        ]
        mock_get.return_value.raise_for_status = Mock()

        result = get_user_repos_with_commit_counts("John567")

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["repo"], "Triangle567")
        self.assertEqual(result[0]["commits"], 10)
        self.assertEqual(result[1]["repo"], "Square567")
        self.assertEqual(result[1]["commits"], 27)

    @patch("github_api.requests.get")
    def test_empty_repos_list(self, mock_get):
        mock_get.return_value.json.return_value = []
        mock_get.return_value.raise_for_status = Mock()

        result = get_user_repos_with_commit_counts("NoReposUser")

        self.assertEqual(result, [])

    @patch("github_api.requests.get")
    def test_user_not_found_returns_empty(self, mock_get):
        mock_get.return_value.raise_for_status.side_effect = (
            requests.exceptions.HTTPError(response=Mock(status_code=404))
        )

        result = get_user_repos_with_commit_counts("NonexistentUser99999")

        self.assertEqual(result, [])

    @patch("github_api.requests.get")
    def test_skips_repo_with_no_name_key(self, mock_get):
        mock_get.return_value.json.side_effect = [
            [{"name": "GoodRepo"}, {"id": 1}],
            [{}] * 5,
        ]
        mock_get.return_value.raise_for_status = Mock()

        result = get_user_repos_with_commit_counts("SomeUser")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["repo"], "GoodRepo")
        self.assertEqual(result[0]["commits"], 5)


class TestGetUserReposWithCommitCountsEdgeCases(unittest.TestCase):

    @patch("github_api.requests.get")
    def test_http_error_returns_empty(self, mock_get):
        mock_get.return_value.raise_for_status.side_effect = (
            requests.exceptions.HTTPError(response=Mock(status_code=403))
        )

        result = get_user_repos_with_commit_counts("AnyUser")

        self.assertEqual(result, [])

    @patch("github_api.requests.get")
    def test_commits_api_failure_returns_zero_for_that_repo(self, mock_get):
        mock_get.return_value.json.side_effect = [
            [{"name": "RepoA"}],
            requests.exceptions.RequestException("network error"),
        ]
        mock_get.return_value.raise_for_status = Mock()

        result = get_user_repos_with_commit_counts("User")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["repo"], "RepoA")
        self.assertEqual(result[0]["commits"], 0)


class TestRun(unittest.TestCase):

    @patch("github_api.get_user_repos_with_commit_counts")
    def test_run_returns_formatted_lines(self, mock_get_repos):
        mock_get_repos.return_value = [
            {"repo": "A", "commits": 1},
            {"repo": "B", "commits": 2},
        ]

        lines = run("testuser")

        self.assertEqual(
            lines,
            [
                "Repo: A Number of commits: 1",
                "Repo: B Number of commits: 2",
            ],
        )
        mock_get_repos.assert_called_once_with("testuser")


if __name__ == "__main__":
    unittest.main()
