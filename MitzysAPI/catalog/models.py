from django.db import models
import string
import random
import base64
import uuid

# Create your models here.
def generate_unique_product_code():
    code = uuid.uuid4().hex

    while Product.objects.filter(product_id=code).exists():
        code = uuid.uuid4().hex
    
    return code

def generate_unique_item_code():
    code = uuid.uuid4().hex

    while Item.objects.filter(item_id=code).exists():
        code = uuid.uuid4().hex
    
    return code


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, default=" ")
    description = models.TextField(max_length=150, default=" ")
    parent = models.ForeignKey('self', 
                                null=True, 
                                on_delete=models.CASCADE,
                                limit_choices_to={'is_child': False})
    is_child = models.BooleanField(default=False)

    class Meta:
        unique_together = ['name', 'parent']

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=30)


    def __str__(self):
        return self.name

class Product(models.Model):
    product_id = models.UUIDField(primary_key=True, default=generate_unique_product_code, editable=False)
    title = models.CharField(max_length=150)
    details = models.TextField(max_length=600, default=" ")
    date_added = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True) # 1 will be the 'General' category.
    sub_category = models.ForeignKey(Category, 
                                    on_delete=models.CASCADE, 
                                    null=True, 
                                    related_name='sub_category',
                                    limit_choices_to={'is_child': True})
    is_available = models.BooleanField(default=True)
    brand = models.ForeignKey(Brand,
                              on_delete=models.PROTECT,
                              null=True,
                              related_name='brand')

    def __str__(self):
        return f'{self.title}'


class Item(models.Model):
    item_id = models.UUIDField(primary_key=True, default=generate_unique_item_code, editable=False)
    size = models.CharField(max_length=30, default="Unavailable")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.product.title} in size {self.size}'



