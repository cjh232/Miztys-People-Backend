from django.db import models
from products.models import Variant
from users.models import User
import uuid


# Create your models here.
def generate_unique_code():
    return uuid.uuid4()


class Order(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=generate_unique_code,
                          unique=True,
                          editable=False)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        related_name="order_owner")
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.id} ({self.quantity})'


class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=generate_unique_code,
                          unique=True,
                          editable=False)

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
