import mock
import pytest


@pytest.mark.django_db
def test_DELETE(client, http_headers, mock_backend_authenticated_client, app_id, make_app):
    """
    @type client: django.test.Client
    @type http_headers: dict
    @type mock_backend_authenticated_client: mock.Mock
    """
    domain = 'example.com'
    with mock.patch('api_server.api.app_domain_details_api_view.get_backend_authenticated_client') as mocked:
        mocked.return_value = mock_backend_authenticated_client
        resp = client.delete(
            '/api/v1/apps/{}/domains/{}/'.format(app_id, domain), **http_headers)
    assert resp.status_code == 204
    mock_backend_authenticated_client.remove_application_domain.asseassert_called_once_with(
        app_id, domain)
