# Generated by Django 3.1.7 on 2021-04-24 17:43

import catalog.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0002_order_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.UUIDField(default=catalog.models.generate_unique_code, editable=False, primary_key=True, serialize=False, unique=True)),
                ('status', models.CharField(choices=[('A', 'Abandoned'), ('F', 'Finished'), ('O', 'Ongoing')], default='O', max_length=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.UUIDField(default=catalog.models.generate_unique_code, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.item')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.order')),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.UUIDField(default=catalog.models.generate_unique_code, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.cart')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.item')),
            ],
        ),
    ]