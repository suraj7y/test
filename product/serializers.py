from django.db.models import Q
from rest_framework import serializers
from product.models import Productmaster


class ProductInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Productmaster
        fields = '__all__'

