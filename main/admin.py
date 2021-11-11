from django.contrib import admin

from .models import *


class ImageInlineAdmin(admin.TabularInline):
    model = Image
    fields = ('image', )
    max_num = 6


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    inlines = [ImageInlineAdmin, ]


admin.site.register(Category)
admin.site.register(User)

