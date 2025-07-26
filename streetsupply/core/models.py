from django.db import models
from django.contrib.auth.models import User

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,  null=True, blank=True) 
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    
    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    average_rating = models.FloatField(default=0.0)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.company_name

class Product(models.Model):
    name = models.CharField(max_length=100)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()
    unit = models.CharField(max_length=50, default='kg')  # or liter, packet, etc.
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)  # new field

    def __str__(self):
        return f"{self.name} - {self.supplier.company_name}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,  null=True, blank=True ) # link order to user
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    delivered = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} by {self.vendor.name} for {self.user.username}"

class Review(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE,  null=True, blank=True)
    rating = models.PositiveSmallIntegerField()  # 1 to 5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
