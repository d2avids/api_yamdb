# Generated by Django 3.2 on 2023-07-04 19:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("reviews", "0002_alter_customuser_confirmation_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="confirmation_code",
            field=models.UUIDField(default="4fed3111-4d9e-4a2d-acc0-3a69e3717578"),
        ),
    ]