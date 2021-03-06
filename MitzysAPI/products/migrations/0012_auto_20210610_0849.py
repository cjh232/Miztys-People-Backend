# Generated by Django 3.1.7 on 2021-06-10 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_auto_20210610_0822'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='category_id',
            new_name='id',
        ),
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='products.category'),
        ),
    ]
