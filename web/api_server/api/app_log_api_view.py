from django.utils.decorators import method_decorator

from api_server.api.api_base_view import ApiBaseView
from api_server.paas_backends import get_backend_authenticated_client
from wsse.decorators import check_wsse_token


@method_decorator(check_wsse_token, 'dispatch')
class AppLogApiView(ApiBaseView):

    def get(self, request, app_id):
        """Get the log for this application

        Returns a JSON list of log entries (str).

        TODO this is not true currently
        Each entry is a string which may contain newline characters

        :param django.http.HttpRequest request: the request object
        :param str app_id: the ID of the app

        :rtype: django.http.HttpResponse
        """
        backend = self.get_backend_for_app(app_id)
        auth_client = get_backend_authenticated_client(
            request.user.username, backend)

        lines = request.GET.get('lines', None)
        if lines is not None:
            lines = int(lines)

        logs = auth_client.get_application_log(app_id, lines)
        return self.respond_multiple(logs)
