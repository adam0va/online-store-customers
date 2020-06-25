from rest_framework.permissions import BasePermission
from customers_app.requesters.authrequester import AuthRequester
from customers_app.requesters.requester import Requester


class BaseAuthPermission(BasePermission):
    def _get_token_from_request(self, request):
        return Requester().get_token_from_request(request)


class CustomerAdminPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        r = AuthRequester()
        response, status_code = r.get_user_info(r.get_token_from_request(request))
        auth_json = r.get_data_from_response(response)

        return int(view.kwargs[view.lookup_url_kwarg]) == auth_json['id'] or auth_json['is_superuser']


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        r = AuthRequester()
        response, status_code = r.get_user_info(r.get_token_from_request(request))
        auth_json = r.get_data_from_response(response)

        return int(view.kwargs[view.lookup_url_kwarg]) == auth_json['is_superuser']


class IsAuthenticated(BaseAuthPermission):
    def has_permission(self, request, view):
        token = self._get_token_from_request(request)
        if token is None:
            return False
        return AuthRequester().is_token_valid(token)[1]


class IsAppTokenCorrect(BaseAuthPermission):
    def has_permission(self, request, view):
        token = self._get_token_from_request(request)
        if token is None:
            return False
        view.app_access_token = token
        return AuthRequester().app_verify_token(token)[1]
