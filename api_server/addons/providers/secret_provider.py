from django.utils import crypto
from uuid import uuid4


class SecretAddonProvider(object):

    config_name = 'SECRET_KEY'

    def begin_provision(self, app_id):
        """Kick off the provision process and return a UUID
        for the new addon. This method MUST return immediately.
        In the event of errors, raise any subclass of AddonProviderError.

        @type app_id: str

        @rtype: dict
            A dictionary with the following keys:
            {
                'message': 'the message to be displayed to the user',
                'uuid': 'the unique ID for this addon. Must be a UUID object.',
            }

        @raises: AddonProviderError
            If the resource cannot be allocated.
        """
        return {
            'message': 'A secret key will be stored into {}.'.format(self.config_name),
            'uuid': uuid4(),
        }

    def wait_for_provision(self, uuid):
        """This method should only return after the provision process
        has ended. In the event that the provision process has already
        completed, just return immediately. That is, this method should
        not assume that it will only be called when provision is taking
        place. As long as the resource is still available, this method
        should work properly. If the resource is no longer available,
        raise AddonProviderInvalidOperationError

        @type uuid: uuid.UUID
            The UUID of the addon, returned from `begin_provision`.

        @rtype: dict
            {
                'config': {
                    'ENV_VAR1': ...
                    ...
                }
            }

        @raises: AddonProviderInvalidOperationError
            If the resource is no longer available, or if the provision
            fails.
        """
        return {
            'config': {
                self.config_name: crypto.get_random_string(length=100)
            }
        }

    def deprovision(self, uuid):
        """Kicks off the deprovision process. This should return right away.

        @type: uuid: uuid.UUID
            The UUID of the addon

        @rtype: dict
            {
                'message': 'The message to be displayed to the user.'
            }

        @raises: AddonProviderError
            If deprovision cannot start, or if it has already started.
        """
        return {
            'message': 'Please remove {} from your config manually.'.format(self.config_name)
        }