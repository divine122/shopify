from django.urls import path
from . import views

urlpatterns = [
    path('product-view/', views.ProductView.as_view()),
    path('products/<int:pk>/', views.UpdateProductView.as_view()),
    path('products/<int:pk>/delete/', views.DeleteProductView.as_view()),
    path('categories/', views.CategoryView.as_view())
]