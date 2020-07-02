from customers_app.requesters.requester import Requester
from customers_app.requesters.authrequester import AuthRequester


class OrdersRequester(Requester):
    #ORDERS_HOST = Requester.HOST + ':8002/'
    ORDERS_HOST = 'https://rsoi-online-store-orders.herokuapp.com/'

    def get_order(self, uuid, token=None):
        headers = {}
        if token:
            headers = AuthRequester()._create_auth_header(token)
        response = self.get_request(self.ORDERS_HOST + str(uuid) + '/', headers=headers)
        if response is None:
            return self.BASE_HTTP_ERROR
        return response, response.status_code

    def delete_order(self, uuid, token=None):
        headers = {}
        if token:
            headers = AuthRequester()._create_auth_header(token)
        response = self.get_request(self.ORDERS_HOST + str(uuid) + '/', headers=headers)
        response = self.delete_request(self.ORDERS_HOST + str(uuid) + '/')
        if response is None:
            return self.BASE_HTTP_ERROR
        return response, response.status_code

    def post_order(self, data={}, token=None):
        headers = {}
        if token:
            headers = AuthRequester()._create_auth_header(token)
        response = self.post_request(url=self.ORDERS_HOST, data=data, headers=headers)
        if response is None:
            return self.BASE_HTTP_ERROR
        return response, response.status_code
