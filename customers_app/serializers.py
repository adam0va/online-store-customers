from rest_framework import serializers
from customers_app.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['name', 'login', 'orders', 'uuid']

    def create(self, validated_data):
        new = Customer(**validated_data)
        new.save()
        return new
