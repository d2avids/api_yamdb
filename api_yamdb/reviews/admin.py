from django.contrib import admin

from .models import Category, Comment, CustomUser, Genre, Review, Title


class TitleAdmin(admin.ModelAdmin):
    search_fields = ("category__slug", "genre__slug", "name", "year")


admin.site.register(CustomUser)
admin.site.register(Title, TitleAdmin)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Comment)
