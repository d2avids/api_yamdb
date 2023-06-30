from django.contrib import admin

from .models import CustomUser, Title, Genre, Category

admin.site.register(CustomUser)
admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(Category)
