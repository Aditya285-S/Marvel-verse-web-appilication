from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Movies)
admin.site.register(Tag)
admin.site.register(Genre)
admin.site.register(Director)
admin.site.register(Actor)
admin.site.register(Comment)