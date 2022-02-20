from django.contrib import admin
from .models import Category, Element, Perfume, Comment


admin.site.register([Category, Element, Perfume, Comment])

