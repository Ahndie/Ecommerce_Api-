from rest_framework import serializers
from .models import Product, Category
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    created_by = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock_quantity', 'image_url', 'created_at', 'category', 'created_by']

    def validate(self, data):
        if data['price'] <= 0:
            raise serializers.ValidationError("Price must be a positive number.")
        if data['stock_quantity'] < 0:
            raise serializers.ValidationError("Stock quantity cannot be negative.")
        return data 