# test/test_client.py
from unittest.mock import Mock

import pytest
import requests

from src.client import MicrosoftIRClient


def test_get_url_content_success():
    client = MicrosoftIRClient()
    url = "http://example.com/report.pdf"

    mock_response = Mock()
    mock_response.raise_for_status = Mock()
    # ensure get returns our mock response
    client._session.get = Mock(return_value=mock_response)

    result = client.get_url_content(url)

    # returned response is the mocked one and raise_for_status was invoked
    assert result is mock_response
    client._session.get.assert_called_once_with(url)
    mock_response.raise_for_status.assert_called_once()


def test_get_url_content_raises():
    client = MicrosoftIRClient()
    url = "http://example.com/bad.pdf"

    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("boom")
    client._session.get = Mock(return_value=mock_response)

    with pytest.raises(requests.HTTPError):
        client.get_url_content(url)

    client._session.get.assert_called_once_with(url)
    mock_response.raise_for_status.assert_called_once()
