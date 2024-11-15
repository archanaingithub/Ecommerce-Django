from django.db import models
from django.contrib.auth import get_user_model
from decimal import Decimal
# Create your models here.

User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=25)

    def __str__(self):
        return self.title


class Product(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=1000)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    inventory = models.IntegerField()
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )
    def __str__(self):
        return self.name
    
    @property
    def price_with_tax(self):
        return self.price + self.price * Decimal(0.13)
    

class Customer(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    contact = models.IntegerField()
    customer = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.first_name} - {self.contact}"


class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    country = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    street_name = models.CharField(max_length=30)


class Order(models.Model):
    PENDING_STATUS = "P"
    COMPLETED_STATUS = "C"
    FAILED_STATUS = "F"

    PAYMENT_STATUS = [
        (PENDING_STATUS, "Pending"),
        (COMPLETED_STATUS, "Completed"),
        (FAILED_STATUS, "Failed"),
    ]

    # PENDING = "P"
    # PROCESSING = 'Processing'
    # SHIPPED = 'S'
    # DELIVERED = "D"
    # CANCELLED = "C"

    # ORDER_STATUS = [
    #     (PENDING, "Pending"),
    #     (PROCESSING, "Processing"),
    #     (SHIPPED, "Shipped"),
    #     (DELIVERED, "Delivered"),
    #     (CANCELLED, "Cancelled"),
    # ]

    place_at = models.DateTimeField(auto_now_add=False)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS, default=PENDING_STATUS
    )
    # order_status = models.CharField(max_length=10,
    #                                 choices=ORDER_STATUS,
    #                                 default=PENDING)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    @property
    def total_amount(self):
        return sum([item.total_price_with_tax for item in self.cart_items.all()])


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="cart_items")
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    quantity = models.IntegerField(default=1)
    price = models.FloatField(default=0.00)
    
    @property
    def total_price(self):
        return self.quantity * self.product.price
    @property
    def total_price_with_tax(self):
        return self.quantity * self.product.price_with_tax
