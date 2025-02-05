from rest_framework import serializers
from .models import Cart,CartItem
from eCommerce.serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  
   

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.total_price  


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.ReadOnlyField()
    total_with_shipping = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total', 'total_with_shipping']

    def get_total(self, obj):
        return obj.total  
    
    def get_total_with_shipping(self,obj):
        return obj.total_with_shipping
