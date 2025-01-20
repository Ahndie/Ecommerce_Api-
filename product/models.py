from django.db import models
from category.models import Category
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()
    image_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True,)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)
    


    def __str__(self):
        return f"{self.name}"
    

    # Ensure stock is reduced on order
    def reduce_stock(self, quantity):
        if self.stock_quantity >= quantity:
            self.stock_quantity -= quantity
            self.save()
        else:
            raise ValueError("Not enough stock")
