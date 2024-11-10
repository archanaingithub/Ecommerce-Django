from django.shortcuts import render
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from . import models
from .serializers import CategorySerializer, ProductSerializer
"""api ko response"""


class CategoryViewSet(ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = CategorySerializer
    
class ProductViewSet(ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = ProductSerializer