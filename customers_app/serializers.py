from rest_framework import serializers
from customers_app.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['name', 'username', 'orders', 'user_id']

    def create(self, validated_data):
        new = Customer(**validated_data)
        new.save()
        return new

    def update(self, instance: Customer, validated_data):
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        return instance


class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50, allow_null=False, allow_blank=False)
    username = serializers.CharField(max_length=50, allow_null=False, allow_blank=False)
    password = serializers.CharField(max_length=50, allow_null=False, allow_blank=False)
