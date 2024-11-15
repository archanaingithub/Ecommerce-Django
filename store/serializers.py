from rest_framework import serializers
from . import models


class CategorySerializer(serializers.ModelSerializer):
    total_product = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Category
        fields = [
            "id",
            "title",
            "total_product",
        ]


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    price = serializers.IntegerField()
    inventory = serializers.IntegerField()

    class Meta:
        model = models.Product
        fields = [
            "id",
            "name",
            "price",
            "inventory",
            "category",
            "description",
            "price_with_tax",
        ]


class CartItemSerializer(serializers.ModelSerializer):
    cart_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Cart.objects.all(), source="cart"
    )
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Product.objects.all(), source="product"
    )

    product = ProductSerializer()

    class Meta:
        model = models.CartItem
        fields = [
            "id",
            "cart_id",
            "product_id",
            "product",
            "quantity",
            "price",
            "total_price",
            "total_price_with_tax",
        ]


class CartSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=models.User.objects.all(),
        source="user",
    )
    user = serializers.StringRelatedField()
    items = CartItemSerializer(many=True)

    class Meta:
        model = models.Cart
        fields = [
            "id",
            "user_id",
            "user",
            "items",
            "total_amount",
        ]


class AddToCartSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    """this to make sure that the data of a logged in user can only be seen by 
        himself only HiddenField is used to automatically set the
        user to the logged-in user
        without them needing to send it.
    """
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Product.objects.all(),
        source="product",
    )

    class Meta:
        model = models.CartItem
        fields = [
            "id",
            "user",
            "product_id",
            "quantity",
        ]

        # there's no user in cart item, but we need to know the cart items
        # of the users
        # we know which user is logged in but we also need to know
        # cart item of that
        # logged in user.

    def create(self, validated_data):
        user = self.validated_data.get("user")
        product = self.validated_data.get("product")
        quantity = self.validated_data.get("quantity")
        
        # if the user has the cart get it,
        # if the user doesn't have cart, create one
        if user is None:
            raise serializers.ValidationError("User is required")

        cart, _ = models.Cart.objects.get_or_create(user=user)

        try:
            cart_item = models.CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=quantity
            )
            cart_item.quantity += 1
            cart_item.save()
            return cart_item
        except models.CartItem.DoesNotExist:
            validated_data.update(
                {
                    "cart": cart,
                }
            )

        return super().create(validated_data)
