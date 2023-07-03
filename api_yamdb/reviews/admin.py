from django.contrib import admin

from .models import CustomUser, Review, Comment

admin.site.register(CustomUser)
admin.site.register(Review)
admin.site.register(Comment)
