# Generated by Django 4.1.5 on 2023-02-16 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_cartitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='contact_number',
            field=models.CharField(default='Null', max_length=12),
        ),
    ]
