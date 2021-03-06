import pytest

from api_server.clients.exceptions import ClientResponseError


@pytest.fixture
def deis_authenticated_client(deis_client, username, password, email):
    deis_client.register(username, password, email)
    return deis_client.login(username, password)


@pytest.fixture
def deis_authenticated_client2(deis_client, username2, password, email2):
    deis_client.register(username2, password, email2)
    return deis_client.login(username2, password)


@pytest.yield_fixture
def create_application(deis_authenticated_client, app_id):
    """
    @type deis_authenticated_client: api_server.clients.deis_authenticated_client.DeisAuthenticatedClient
    """
    deis_authenticated_client.create_application(app_id)
    try:
        yield
    finally:
        deis_authenticated_client.delete_application(app_id)


def test_application_creation(deis_authenticated_client, app_id):
    """
    @type deis_authenticated_client: api_server.clients.deis_authenticated_client.DeisAuthenticatedClient
    """
    # create application
    deis_authenticated_client.create_application(app_id)

    with pytest.raises(ClientResponseError):
        deis_authenticated_client.create_application(app_id)

    ids = deis_authenticated_client.get_all_applications()
    assert ids == [app_id]

    # delete application
    deis_authenticated_client.delete_application(app_id)

    ids = deis_authenticated_client.get_all_applications()
    assert ids == []

    with pytest.raises(ClientResponseError):
        deis_authenticated_client.delete_application(app_id)


def test_application_env_variables(deis_authenticated_client, app_id, create_application):
    """
    @type deis_authenticated_client: api_server.clients.deis_authenticated_client.DeisAuthenticatedClient
    """
    # test environmental variables
    bindings = {
        'TESTING1': '1',
        'TESTING2': '2'
    }
    old_vars = deis_authenticated_client.get_application_env_variables(app_id)
    deis_authenticated_client.set_application_env_variables(
        app_id, bindings)

    old_vars_updated = old_vars.copy()
    old_vars_updated.update(bindings)

    new_vars = deis_authenticated_client.get_application_env_variables(app_id)
    assert new_vars == old_vars_updated

    deis_authenticated_client.set_application_env_variables(
        app_id, {key: None for key in bindings})
    new_vars_deleted = deis_authenticated_client.get_application_env_variables(
        app_id)
    assert old_vars == new_vars_deleted

    # test deletion and creation at the same time
    deis_authenticated_client.set_application_env_variables(
        app_id, {"TESTING1": '1'})
    deis_authenticated_client.set_application_env_variables(
        app_id, {"TESTING1": None, "TESTING2": "2"})
    assert deis_authenticated_client.get_application_env_variables(app_id) == {
        'TESTING2': '2'
    }


def test_application_domains(deis_authenticated_client, app_id, create_application):
    domain = '{}.example.com'.format(app_id)
    old_domains = deis_authenticated_client.get_application_domains(app_id)
    deis_authenticated_client.add_application_domain(app_id, domain)
    assert deis_authenticated_client.get_application_domains(
        app_id) == old_domains + [domain]

    # can't add a domain twice
    with pytest.raises(ClientResponseError):
        deis_authenticated_client.add_application_domain(app_id, domain)

    deis_authenticated_client.remove_application_domain(app_id, domain)
    assert deis_authenticated_client.get_application_domains(
        app_id) == old_domains

    # can't remove a non-existent domain
    with pytest.raises(ClientResponseError):
        deis_authenticated_client.remove_application_domain(app_id, domain)


def test_run_command(deis_authenticated_client, app_id, create_application):
    """
    @type deis_authenticated_client: api_server.clients.deis_authenticated_client.DeisAuthenticatedClient
    """
    # this will fail because we don't have a build associated with this app,
    # and it takes too long to create a build to do this in testing
    with pytest.raises(ClientResponseError):
        deis_authenticated_client.run_command(app_id, 'echo 1 2 3')


def test_application_ownership(deis_authenticated_client, app_id, create_application, deis_authenticated_client2, username, username2):
    """
    @type deis_authenticated_client: api_server.clients.deis_authenticated_client.DeisAuthenticatedClient
    @type deis_authenticated_client2: api_server.clients.deis_authenticated_client.DeisAuthenticatedClient
    """
    assert deis_authenticated_client.get_application_owner(app_id) == username

    deis_authenticated_client.set_application_owner(app_id, username2)
    with pytest.raises(ClientResponseError):
        deis_authenticated_client.get_application_owner(
            app_id)  # no permissions

    deis_authenticated_client2.get_application_owner(app_id) == username2

    # set the ownership back so the fixture can delete the application
    deis_authenticated_client2.set_application_owner(app_id, username)


def test_application_collaborators(deis_authenticated_client, app_id, create_application, deis_authenticated_client2, username, username2):
    """
    @type deis_authenticated_client: api_server.clients.deis_authenticated_client.DeisAuthenticatedClient
    @type deis_authenticated_client2: api_server.clients.deis_authenticated_client.DeisAuthenticatedClient
    """
    assert deis_authenticated_client.get_application_collaborators(app_id) == [
    ]

    # add collaborator
    deis_authenticated_client.add_application_collaborator(app_id, username2)
    assert deis_authenticated_client.get_application_collaborators(app_id) == [
        username2]

    # check if collaborator actually has some permissions
    deis_authenticated_client2.get_application_owner(app_id) == username
    # ...but not all permissions
    with pytest.raises(ClientResponseError):
        deis_authenticated_client2.set_application_owner(app_id, username2)

    # remove collaborator
    deis_authenticated_client.remove_application_collaborator(
        app_id, username2)
    assert deis_authenticated_client.get_application_collaborators(app_id) == [
    ]
    with pytest.raises(ClientResponseError):
        deis_authenticated_client.remove_application_collaborator(
            app_id, username2)

    # no longer has any permissions
    with pytest.raises(ClientResponseError):
        deis_authenticated_client2.get_application_owner(app_id)


def test_log(deis_authenticated_client, app_id, create_application):
    """
    @type deis_authenticated_client: api_server.clients.deis_authenticated_client.DeisAuthenticatedClient
    """
    domain = '{}.example.com'.format(app_id)
    deis_authenticated_client.add_application_domain(app_id, domain)
    deis_authenticated_client.remove_application_domain(app_id, domain)
    logs = deis_authenticated_client.get_application_logs(app_id, 2)
    assert len(logs) == 2
    logs = deis_authenticated_client.get_application_logs(app_id)
    assert len(logs) == 3


def test_keys(deis_authenticated_client, public_key):
    """
    @type deis_authenticated_client: api_server.clients.deis_authenticated_client.DeisAuthenticatedClient
    """
    key_name = 'key_name'
    old_keys = deis_authenticated_client.get_keys()

    deis_authenticated_client.add_key(key_name, public_key)
    new_keys = deis_authenticated_client.get_keys()
    assert new_keys == old_keys + [{'key_name': key_name, 'key': public_key}]

    with pytest.raises(ClientResponseError):
        deis_authenticated_client.add_key(key_name, public_key)

    deis_authenticated_client.remove_key(key_name)
    assert deis_authenticated_client.get_keys() == old_keys

    with pytest.raises(ClientResponseError):
        deis_authenticated_client.remove_key(key_name)
