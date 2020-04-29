from rest_framework import status
from rest_framework.views import Response, Request, APIView
from customers_app.models import Customer
from customers_app.serializers import CustomerSerializer
from rest_framework.generics import ListCreateAPIView


class CustomerList(ListCreateAPIView):
    serializer_class = CustomerSerializer

    def get_queryset(self):
        return Customer.objects.all()


class CustomerDetail(APIView):
    def get(self, request, uuid):
        try:
            reader = Customer.objects.get(pk=uuid)
        except Customer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CustomerSerializer(reader)
        return Response(serializer.data, status=status.HTTP_200_OK)

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