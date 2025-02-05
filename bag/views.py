from django.shortcuts import render
from . serializers import CartItemSerializer,CartSerializer
from . models import Cart,CartItem
from  rest_framework import status,permissions,views
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser,FormParser,JSONParser
from eCommerce.models import Product

# Create your views here.




            
class CartView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser,MultiPartParser, FormParser]

    @swagger_auto_schema(responses={200: CartSerializer})
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response({
            "cart": serializer.data,
            "total": cart.total,
            "total_with_shipping": cart.total_with_shipping
        }, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=CartItemSerializer)
    def post(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(request_body=CartItemSerializer)
    def delete(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')

        try:
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            cart_item.delete()
            return Response({"detail": "Item removed from cart"}, status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({"detail": "Item not found in cart"}, status=status.HTTP_404_NOT_FOUND)