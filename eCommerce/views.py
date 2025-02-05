from django.shortcuts import render
from . models import Category,Product
from . serializers import ProductSerializer,CategorySerializer
from rest_framework import status,response,views,permissions
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework.response import Response
from rest_framework.decorators import action

# Create your views here.


class ProductView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductSerializer
    parser_classes = (MultiPartParser,FormParser)

    @swagger_auto_schema(request_body=ProductSerializer)
    def post(self,request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'product created sucessfully', 'product':serializer.data}, status=201)
        

        return Response(serializer.errors, status=400)
    
    def get(self,request):
        products = Product.objects.all()
        serializer = self.serializer_class(products, many=True)
        return Response(serializer.data, status=200)
    

class UpdateProductView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self,request,pk,*args,**kwargs):
        try:
            product = Product.objects.get(pk=pk)

        except Product.DoesNotExist:
            return Response({'detail':'product not found'}, status=status.HTTP_404_NOT_FOUND)    
        

        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Product updated successfully', 'product': serializer.data}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class DeleteProductView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self,request,pk,*args,**kwargs):
        try:
            product = Product.objects.get(pk=pk)

        except Product.DoesNotExist:
            return Response({'detail':'product not found'}, status=status.HTTP_404_NOT_FOUND)


        product.delete()
        return Response({'detail':'product deleted successfully'}, status=status.HTTP_200_OK)


class CategoryView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CategorySerializer

    @swagger_auto_schema(request_body=CategorySerializer)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
    
            serializer.save()
            return Response(
                {'message': 'Category created successfully', 'category': serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def get(self, request):
        categories = Category.objects.all()
        serializer = self.serializer_class(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)   

