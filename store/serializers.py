from rest_framework import serializers
from . import models

class CategorySerializer(serializers.ModelSerializer):
    total_product = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = models.Category
        fields = [
            "title",
            "total_product",
        ]
    

class ProductSerializer(serializers.ModelSerializer):
    price = serializers.IntegerField()
    inventory = serializers.IntegerField()
    class Meta:
        model = models.Product
        fields = [
            "name",
            "price",
            "inventory",
            "category",
            "description",
        ]