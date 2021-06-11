from django.db import models
import uuid


def generate_unique_product_code():
    return uuid.uuid4().hex[:6].upper()

def generate_unique_code():
    return uuid.uuid4()

def generate_product_slug(title):
    return title

class Color(models.Model):
    name = models.CharField(max_length=15)

    class Meta:
        unique_together = ['name',]

    def __str__(self):
        return f'{self.name}'

class Size(models.Model):
    type = models.CharField(max_length=30)
    value = models.CharField(max_length=10)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['type', 'value']

    def __str__(self):
        return f'{self.type}: {self.value}'

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, default=" ")
    desc = models.TextField(
                        max_length=150,
                        null=True,
                        blank=True, 
                        default=" ")
    parent = models.ForeignKey('self', 
                        on_delete=models.CASCADE,
                        null=True, 
                        related_name='children',
                        blank=True,
                        limit_choices_to={'parent': None},
                        default=None)

    class Meta:
        unique_together =['name', ]
        verbose_name_plural = 'Categories'

    def products_count(self):
        return Product.objects.filter(
            models.Q(category=self) | models.Q(sub_category=self)
        ).count()

    def __str__(self):
        return self.name

    def breadcrumb(self):
        return f'{self.parent.name} / {self.name}' if self.parent is not None else self.name


class Brand(models.Model):
    name = models.CharField(max_length=30)

    def products_count(self):
        return Product.objects.filter(brand=self).count()

    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.CharField(primary_key=True,
                               default=generate_unique_product_code, 
                               unique=True, 
                               editable=False,
                               max_length=30)
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=200)
    details = models.TextField(max_length=600, default=" ", null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True) # 1 will be the 'General' category.
    sub_category = models.ForeignKey(Category, 
                                    on_delete=models.CASCADE, 
                                    null=True, 
                                    related_name='sub_category',
                                    limit_choices_to={'parent__isnull': False})
    is_available = models.BooleanField(default=True)
    brand = models.ForeignKey(Brand,
                              on_delete=models.PROTECT,
                              null=True,
                              related_name='brand')

    def __str__(self):
        return f'{self.title}'

    def available_colors(self):
        variants = Variant.objects.filter(product=self, quantity__gte=1)

        return variants.distinct("color").values_list('color__name',  flat=True)

class Variant(models.Model):
    id = models.UUIDField(primary_key=True,
                               default=generate_unique_code, 
                               unique=True,
                               editable=False)

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    size = models.ForeignKey(Size, on_delete=models.PROTECT)
    color = models.ForeignKey(Color, on_delete=models.PROTECT)

    quantity = models.IntegerField(default=1)
    is_available = models.BooleanField(default=True)

    def category(self):
        return self.product.category

    def sub_category(self):
        return self.product.sub_category

    def brand(self):
        return self.product.brand

    def __str__(self):
        return f'{self.product.title} in size {self.size} in color {self.color}'

    class Meta:
        unique_together =['product', 'size', 'color']
