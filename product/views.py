from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Product
from .serializers import ProductSerializer
from django_filters import rest_framework as filters
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters



# Create your views here.
def product(request):
    return HttpResponse("Shop with us!")

# Custom pagination
class ProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# Product viewset
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users
    pagination_class = ProductPagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['category__name', 'price', 'stock_quantity']
    ordering_fields = ['name', 'price', 'created_at']

    def perform_create(self, serializer):
        # Associate product with the authenticated user
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'], url_path='search')
    def search_products(self, request):
        search_query = request.query_params.get('q', '')
        products = Product.objects.filter(name__icontains=search_query)
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


# User Management view (for User CRUD)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class UserCreateView(APIView):
    def post(self, request):
        # User registration
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.create_user(username=username, email=email, password=password)
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
    def post(self, request):
        # User login
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
    