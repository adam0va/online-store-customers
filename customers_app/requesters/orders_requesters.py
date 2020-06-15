from customers_app.requesters.requester import Requester


class OrdersRequester(Requester):
    ORDERS_HOST = Requester.HOST + ':8002/'

    def get_order(self, uuid):
        response = self.get_request(self.ORDERS_HOST + str(uuid) + '/')
        if response is None:
            return self.BASE_HTTP_ERROR
        return response, response.status_code

    def delete_order(self, uuid):
        response = self.delete_request(self.ORDERS_HOST + str(uuid) + '/')
        if response is None:
            return self.BASE_HTTP_ERROR
        return self.get_data_from_response(response), response.status_code