from customers_app.requesters.requester import Requester


class OrdersRequester(Requester):
    ORDERS_HOST = Requester.HOST + ':8002/'
    #ORDERS_HOST = 'https://rsoi-online-store-orders.herokuapp.com/'

    def get_order(self, uuid):
        response = self.get_request(self.ORDERS_HOST + str(uuid) + '/')
        if response is None:
            return self.BASE_HTTP_ERROR
        return response, response.status_code

    def delete_order(self, uuid):
        response = self.delete_request(self.ORDERS_HOST + str(uuid) + '/')
        if response is None:
            return self.BASE_HTTP_ERROR
        return response, response.status_code

    def post_order(self, data={}):
        response = self.post_request(url=self.ORDERS_HOST, data=data)
        if response is None:
            return self.BASE_HTTP_ERROR
        return response, response.status_code
