# Generated by Django 4.1.5 on 2023-02-02 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(default='null', max_length=50),
        ),
    ]