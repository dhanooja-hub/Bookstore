from django.contrib import admin

# Register your models here.
from books.models import Language

from books.models import Tag

from books.models import Category

from books.models import Product

admin.site.register(Product)

admin.site.register(Language)

admin.site.register(Tag)

admin.site.register(Category)