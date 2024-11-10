from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "total_product",
    ]
    list_display_links = (
        "title",
    )
    search_fields = [
        "title",
    ]
    
    def total_product(self, category):
        return category.products.count()
    
    def get_queryset(self, request):
        return super().get_queryset(request)
    
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "price",
        "stock",
        "category",
    ]
    list_editable = [
        "price",
    ]
    search_fields = [
        "name",
        "category",
        "price",
    ]
    autocomplete_fields = [
        "category",
    ]
    
    def stock(self, product):
        if product.inventory == 0:
            return "Stock empty"
        return f"{product.inventory} items"
    
    
admin.site.register(models.Customer)

class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    

class CartItemInline(admin.TabularInline):
    model = models.CartItem
    extra = 1
    
@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]