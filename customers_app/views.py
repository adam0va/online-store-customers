from rest_framework import status
from rest_framework.views import Response, Request, APIView
from customers_app.models import Customer
from customers_app.serializers import CustomerSerializer, RegisterSerializer
from customers_app.requesters.orders_requesters import OrdersRequester
from customers_app.requesters.requester import Requester
from customers_app.requesters.authrequester import AuthRequester
from customers_app.permissions import CustomerAdminPermission, IsSuperuser, IsAuthenticated
'''
8003 порт
Информация о покупателе включает в себя информацию о его заказах.
Таким образом, при GET запросе, необходимо обращаться
также к сервису заказов.
При PATCH, POST запросах обращение к сервису заказов не требуется, 
поскольку они существуют независимо от того от изменения профиля покупателя,
и появляются не сразу при создании его профиля.
При DELETE запросе заказы покупателя должны удаляться.
'''


class AllCustomersList(APIView):
    ORDER_REQUESTER = OrdersRequester()
    #permission_classes = (IsSuperuser,)

    def get(self, request):
        print(self.ORDER_REQUESTER.get_token_from_request(request))
        customers = Customer.objects.all()
        serialized_customers = [CustomerSerializer(customer).data for customer in customers]
        for customer in serialized_customers:
            if customer['orders']:
                for i in range(len(customer['orders'])):
                    order_response, order_status_code = self.ORDER_REQUESTER.get_order(uuid=customer['orders'][i])
                    print(order_response)
                    if order_status_code == 200:
                        customer['orders'][i] = order_response.json()
        return Response(serialized_customers, status=status.HTTP_200_OK)


class CustomerDetail(APIView):
    ORDER_REQUESTER = OrdersRequester()
    permission_classes = (IsAuthenticated,)
    lookup_field = 'user_id'
    lookup_url_kwarg = 'user_id'

    def get(self, request, user_id):
        try:
            customer = Customer.objects.get(pk=user_id)
        except Customer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serialized = CustomerSerializer(customer)
        serialized_data = serialized.data
        if serialized_data['orders']:
            token = Requester().get_token_from_request(request)
            for i in range(len(serialized_data['orders'])):
                order_response, order_status_code = self.ORDER_REQUESTER.get_order(uuid=serialized_data['orders'][i], token=token)
                if order_status_code == 200:
                    serialized_data['orders'][i] = order_response.json()
        return Response(serialized_data, status=status.HTTP_200_OK)

    def patch(self, request, user_id):
        try:
            customer = Customer.objects.get(pk=user_id)
        except Customer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CustomerSerializer(instance=customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        try:
            customer = Customer.objects.get(user_id=user_id)
        except Customer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if customer.orders:
            token = Requester().get_token_from_request(request)
            for order in customer.orders:
                order_response, order_status_code = self.ORDER_REQUESTER.delete_order(uuid=order, token=token)
                if order_status_code != 204:
                    print(order_status_code)
                    return Response(status=status.HTTP_404_NOT_FOUND)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RegisterView(APIView):
    def post(self, request):
        serialized = RegisterSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        response, status_code = AuthRequester().register(request.data['username'], request.data['password'])
        print(response, status_code)
        if status_code == Requester().BASE_HTTP_ERROR or status_code != 201:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        data_from_response = Requester().get_data_from_response(response)
        print(response.json())
        user_info, user_status_code = AuthRequester().get_user_info(data_from_response['access'])
        if user_status_code != 200:
            return Response(status=status_code)
        user_info_data = Requester().get_data_from_response(user_info)
        # при создании пользователя должен создаваться пустой заказ
        # (а к нему пустой биллинг)
        order_response, order_status_code = OrdersRequester().post_order()
        if order_status_code == 201:
            order_data = Requester().get_data_from_response(order_response)
            order_uuid = order_data['uuid']
            customer = Customer.objects.create(user_id=user_info_data['id'], name=request.data['name'],
                                               username=request.data['username'], orders=[order_uuid])
        else:
            customer = Customer.objects.create(user_id=user_info_data['id'], name=request.data['name'],
                                               username=request.data['username'])
        customer_json = CustomerSerializer(instance=customer).data
        ret_data = {'token': data_from_response, 'user': user_info_data, 'customer': customer_json}
        return Response(ret_data, 201)


class NewOrderForCustomer(APIView):
    ORDER_REQUESTER = OrdersRequester()
    permission_classes = (IsAuthenticated, )

    def get(self, request, user_id):
        try:
            customer = Customer.objects.get(user_id=user_id)
            print(1111)
        except Customer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        token = Requester().get_token_from_request(request)
        new_order_response, new_order_status_code = self.ORDER_REQUESTER.post_order(token=token)
        if new_order_status_code != 201:
            return Response(status=new_order_status_code)
        new_order_response_data = self.ORDER_REQUESTER.get_data_from_response(new_order_response)
        new_order_uuid = new_order_response_data['uuid']
        serializer = CustomerSerializer(instance=customer).data
        old_orders = serializer['orders']
        if old_orders:
            old_orders.append(new_order_uuid)
        else:
            old_orders = [new_order_uuid]
        new_orders = {'orders':old_orders}
        print(new_orders)
        serializer = CustomerSerializer().update(instance=customer, validated_data=new_orders)

        return Response(new_order_response_data, status=status.HTTP_200_OK)
