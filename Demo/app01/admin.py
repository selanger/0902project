from django.contrib import admin
from .models import *

# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_display = ['name',"num"]
    search_fields = ["name"]
    # list_filter = ["name"]
    list_filter = ["num"]



admin.site.register(User)
admin.site.register(HomeNew)
admin.site.register(Book,BookAdmin)
admin.site.register(Publish)
