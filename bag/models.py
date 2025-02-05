from django.db import models
from django.conf import settings
from eCommerce.models import Product

# Create your models here.

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
     return f"Cart of {self.user.first_name}"

    @property
    def total(self):
        return sum(item.total_price for item in self.items.all()) 
    
    @property
    def total_with_shipping(self):
        shipping_cost = 10
        return self.total + shipping_cost


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} * {self.quantity}"

    @property
    def total_price(self):
        return self.product.price * self.quantity  
