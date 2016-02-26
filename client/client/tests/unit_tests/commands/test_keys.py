from tigerhost.entry import entry


def test_add_key(runner, fake_api_client, saved_user, public_key, public_key_path):
    key_name = 'key_name'
    result = runner.invoke(entry, ['keys:add', key_name, public_key_path])
    assert result.exit_code == 0
    fake_api_client.add_key.assert_called_once_with(key_name, public_key)


def test_add_key_nonexistent(runner, fake_api_client, saved_user, public_key, public_key_path):
    key_name = 'key_name'
    result = runner.invoke(
        entry, ['keys:add', key_name, public_key_path + 'blah'])
    assert result.exit_code == 2


def test_list_key(runner, fake_api_client, saved_user):
    keys = [{
        'key_name': 'key1',
        'key': 'ssh-rsa1',
    },
        {
        'key_name': 'key2',
        'key': 'ssh-rsa2',
    },
    ]
    fake_api_client.get_keys.return_value = keys
    result = runner.invoke(entry, ['keys'])
    assert result.exit_code == 0
    for k in keys:
        for _, v in k.iteritems():
            assert v in result.output


def test_remove_key(runner, fake_api_client, saved_user):
    key_name = 'key_name'
    result = runner.invoke(entry, ['keys:remove', key_name])
    assert result.exit_code == 0
    fake_api_client.remove_key.assert_called_once_with(key_name)
