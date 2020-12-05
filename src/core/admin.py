from django.contrib import admin

from .models import Post, Stock, Symbol

admin.site.register(Post)
admin.site.register(Stock)
admin.site.register(Symbol)
