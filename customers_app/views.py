from rest_framework import status
from rest_framework.views import Response, Request, APIView
from customers_app.models import Customer
from customers_app.serializers import CustomerSerializer
from customers_app.requesters.orders_requesters import OrdersRequester
from rest_framework.generics import ListCreateAPIView
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

class CustomerList(ListCreateAPIView):
    serializer_class = CustomerSerializer

    def get_queryset(self):
        return Customer.objects.all()


class CustomerDetail(APIView):
    ORDER_REQUESTER = OrdersRequester()

    def get(self, request, **kwagrs):
        if 'uuid' in kwagrs:
            uuid = kwagrs['uuid']
            try:
                customer = Customer.objects.get(pk=uuid)
            except Customer.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serialized = CustomerSerializer(customer)
            serialized_data = serialized.data
            if serialized_data['orders']:
                for i in range(len(serialized_data['orders'])):
                    order_response = self.ORDER_REQUESTER.get_order(uuid=serialized_data['orders'][i])
                    serialized_data['orders'][i] = order_response[0].json()
            return Response(serialized_data, status=status.HTTP_200_OK)
        else:
            customers = Customer.objects.all()
            serialized_customers = [CustomerSerializer(customer).data for customer in customers]
            for customer in serialized_customers:
                if customer['orders']:
                    for i in range(len(customer['orders'])):
                        order_response = self.ORDER_REQUESTER.get_order(uuid=customer['orders'][i])
                        customer['orders'][i] = order_response[0].json()
            return Response(serialized_customers, status=status.HTTP_200_OK)



    def patch(self, request, uuid):
        try:
            reader = Customer.objects.get(pk=uuid)
        except Customer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CustomerSerializer(instance=reader, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid):
        try:
            reader = Customer.objects.get(uuid=uuid)
        except Customer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        reader.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)