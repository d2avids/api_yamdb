# Generated by Django 3.2 on 2023-07-04 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='confirmation_code',
            field=models.UUIDField(default='bac21299-a30f-4b63-9312-b2211383baf6'),
        ),
    ]
