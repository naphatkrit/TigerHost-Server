import responses
import pytest
import urlparse

from api_server.clients.deis_authenticated_client import DeisAuthenticatedClient


@pytest.fixture
def deis_authenticated_client(fake_deis_url, token):
    return DeisAuthenticatedClient(fake_deis_url, token)


@responses.activate
def test_get_all_applications_success(deis_authenticated_client, fake_deis_url):
    """
    @type deis_authenticated_client: DeisAuthenticatedClient
    @type fake_deis_url: str
    """
    test_ids = ['testid1', 'testid2']
    responses.add(responses.GET, urlparse.urljoin(
        fake_deis_url, 'v1/apps'), status=200, json={
        "results": [{'id': x} for x in test_ids]}
    )
    ids = deis_authenticated_client.get_all_applications()
    assert set(ids) == set(test_ids)


@responses.activate
def test_create_application_success(deis_authenticated_client, fake_deis_url):
    """
    @type deis_authenticated_client: DeisAuthenticatedClient
    @type fake_deis_url: str
    """
    responses.add(responses.POST, urlparse.urljoin(
        fake_deis_url, 'v1/apps/'), status=201)
    deis_authenticated_client.create_application('testid')
