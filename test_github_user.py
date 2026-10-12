from unittest.mock import Mock, patch

import pytest
import requests

from github_user import get_public_repos_count

def make_response(status_code,json_data=None):
    response = Mock()
    response.status_code = status_code
    response.json.return_value = json_data or {}
    if status_code >= 400:
        response.raise_for_status.side_effect = requests.HTTPError("error")
    return response

def test_returns_public_repos_count():
    with patch("github_user.requests.get", return_value=make_response(200, {"public_repos": 7})):
        assert get_public_repos_count("vsayyan") == 7

def test_unknown_user_raises_value_error():
    with patch("github_user.requests.get", return_value=make_response(404)):
        with pytest.raises(ValueError, match="not found"):
            get_public_repos_count("nobody")

def test_server_error_raises_http_error():
    with patch("github_user.requests.get", return_value=make_response(500)):
        with pytest.raises(requests.HTTPError):
            get_public_repos_count("vsayyan")

def test_calls_the_correct_url():
    with patch("github_user.requests.get", return_value=make_response(200, {"public_repos": 1})) as mock_get:
        get_public_repos_count("vsayyan")
    mock_get.assert_called_once_with("https://api.github.com/users/vsayyan", timeout=10)