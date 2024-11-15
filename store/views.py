from django.shortcuts import render

# from rest_framework.decorators import api_view
# from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from . import models
from .pagination import CustomPagination
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    CartItemSerializer,
    CartSerializer,
    AddToCartSerializer,
)
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter
from django.db.models import Prefetch
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import GenericViewSet

"""api ko response"""


class CategoryViewSet(ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CustomPagination
    permission_classes = [
        IsAuthenticated,
    ]


class ProductViewSet(ReadOnlyModelViewSet):
    queryset = models.Product.objects.select_related("category","supplier").all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]


class CartViewSet(GenericViewSet, ListAPIView):
    queryset = models.Cart.objects.prefetch_related(
        Prefetch(
            "cart_items",
            queryset=models.CartItem.objects.all(),
            to_attr="items",
        )
    ).all()
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = CartSerializer

    def get_queryset(self):
        user = self.request.user  # logged in user
        return self.queryset.filter(user=user)
    
    # this to ensure that only logged in user can have a cart

    # no need to have pagination in cart as cart is a sole item carrying numbers of cart items


class CartItemViewSet(ModelViewSet):
    queryset = models.CartItem.objects.all()
    
    serializer_class = CartItemSerializer
    
    def get_queryset(self):
        user = self.request.user
        print("Logged-in user: ", user)
        return self.queryset.filter(cart__user=user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddToCartSerializer
        return CartItemSerializer