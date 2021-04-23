# Generated by Django 3.1.7 on 2021-04-21 00:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_auto_20210420_1705'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='cat_id',
            new_name='category_id',
        ),
        migrations.RenameField(
            model_name='category',
            old_name='cat_name',
            new_name='category_name',
        ),
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.CharField(default=' ', max_length=150),
        ),
        migrations.AddField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.category'),
        ),
    ]