from django.utils.decorators import method_decorator

from api_server.api.api_base_view import ApiBaseView
from api_server.paas_backends import get_backend_authenticated_client
from wsse.decorators import check_wsse_token


@method_decorator(check_wsse_token, 'dispatch')
class AppCollaboratorDetailsApiView(ApiBaseView):

    def delete(self, request, app_id, username):
        """Remove a collaborator from the app

        :param django.http.HttpRequest request: the request
        :param str app_id: the app ID
        :param str username: the username of the collaborator

        :rtype: django.http.HttpResponse
        """
        backend = self.get_backend_for_app(app_id)
        auth_client = get_backend_authenticated_client(
            request.user.username, backend)

        auth_client.remove_application_collaborator(app_id, username)
        return self.respond()
