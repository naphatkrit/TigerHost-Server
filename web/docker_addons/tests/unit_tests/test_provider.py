import docker
import mock
import pytest
import uuid

from api_server.addons.providers.exceptions import AddonProviderError

from docker_addons.containers.base import BaseContainer
from docker_addons.models import ContainerInfo
from docker_addons.provider import DockerAddonProvider


@pytest.yield_fixture(autouse=True)
def fake_docker_client():
    with mock.patch('docker_addons.provider.create_client') as mocked:
        # not actually used, so return a mock object that can't do anything
        mocked.return_value = mock.Mock()
        yield


@pytest.fixture(scope='function')
def fake_type():
    return mock.MagicMock()


@pytest.fixture(scope='function')
def fake_container(fake_type):
    container = mock.Mock(spec=BaseContainer)
    fake_type.get_container.return_value = container
    return container


@pytest.fixture(scope='function')
def provider(fake_type):
    return DockerAddonProvider(fake_type, 'DATABASE_URL')


@pytest.fixture(scope='function')
def fake_container_info():
    info = mock.Mock(spec=ContainerInfo)
    info.uuid = uuid.uuid4()
    return info


def test_begin_provision_success(provider, fake_container_info, fake_container):
    with mock.patch('docker_addons.provider.ContainerInfo.objects.create') as mocked:
        mocked.return_value = fake_container_info
        result = provider.begin_provision(None)
    assert 'message' in result
    assert result['uuid'] == fake_container_info.uuid
    fake_container.run_container.assert_called_once_with()


def test_begin_provision_errors(provider, fake_container_info, fake_container):
    fake_container.run_container.side_effect = docker.errors.DockerException
    with mock.patch('docker_addons.provider.ContainerInfo.objects.create') as mocked:
        mocked.return_value = fake_container_info
        with pytest.raises(AddonProviderError):
            provider.begin_provision(None)


def test_get_config_success(provider, fake_container_info, fake_container):
    url = 'url'
    fake_container.get_url.return_value = url
    with mock.patch('docker_addons.provider.ContainerInfo.objects.get') as mocked:
        mocked.return_value = fake_container_info
        result = provider.get_config(None)
    assert result['config']['DATABASE_URL'] == url
    fake_container.get_url.assert_called_once_with()


def test_get_config_success_with_config_customization(provider, fake_container_info, fake_container):
    url = 'url'
    fake_container.get_url.return_value = url
    with mock.patch('docker_addons.provider.ContainerInfo.objects.get') as mocked:
        mocked.return_value = fake_container_info
        result = provider.get_config(None, config_customization='TEST')
    assert result['config']['TEST_DATABASE_URL'] == url
    fake_container.get_url.assert_called_once_with()


def test_get_config_error(provider, fake_container_info, fake_container):
    with mock.patch('docker_addons.provider.ContainerInfo.objects.get') as mocked:
        mocked.side_effect = ContainerInfo.DoesNotExist
        with pytest.raises(AddonProviderError):
            provider.get_config(None)


def test_deprovision_success(provider, fake_container_info, fake_container):
    with mock.patch('docker_addons.provider.ContainerInfo.objects.get') as mocked:
        mocked.return_value = fake_container_info
        result = provider.deprovision(None)
    assert 'message' in result
    fake_container.stop_container.assert_called_once_with()


def test_deprovision_error(provider, fake_container_info, fake_container):
    with mock.patch('docker_addons.provider.ContainerInfo.objects.get') as mocked:
        mocked.return_value = fake_container_info
        mocked.side_effect = ContainerInfo.DoesNotExist
        with pytest.raises(AddonProviderError):
            provider.deprovision(None)
