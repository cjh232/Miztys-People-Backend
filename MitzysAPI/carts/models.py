from django.db import models
import uuid
from users.models import User
from products.models import Product, Item


# Create your models here.
def generate_unique_code():
    return uuid.uuid4()

class Cart(models.Model):
    id = models.UUIDField(primary_key=True,
                               default=generate_unique_code, 
                               unique=True,
                               editable=False)

    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=False,
        related_name="cart_owner")
    
    ABANDONED = 'A'
    FINISHED = 'F'
    ONGOING = 'O'
    
    STATUS_CHOICES = [
        (ABANDONED, 'Abandoned'),
        (FINISHED,  'Finished'),
        (ONGOING,  'Ongoing'),
    ]

    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=ONGOING
    )

    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    id = models.UUIDField(primary_key=True,
                               default=generate_unique_code, 
                               unique=True,
                               editable=False)

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        null=True
    )
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)