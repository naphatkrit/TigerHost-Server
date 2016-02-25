import pytest

import random
import string

from tigerhost.api_client import ApiClient, ApiClientAuthenticationError


@pytest.fixture(scope='function')
def app_id():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(12))


@pytest.fixture(scope='function')
def api_client(api_server_url, username, api_key):
    return ApiClient(api_server_url=api_server_url, username=username, api_key=api_key)


def test_authentication_failure(api_client):
    api_client.api_key = '123'
    with pytest.raises(ApiClientAuthenticationError):
        api_client.get_all_applications()


def test_application(api_client, app_id):
    """
    @type api_client: ApiClient
    """
    ids = api_client.get_all_applications()
    assert ids == []