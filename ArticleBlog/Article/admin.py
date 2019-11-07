from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Author)
admin.site.register(Type)
admin.site.register(Article)

