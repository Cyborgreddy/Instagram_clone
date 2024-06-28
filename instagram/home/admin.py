from django.contrib import admin

# Register your models here.
from . models import Post,Profile,Like,Comment

admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Like)
admin.site.register(Comment)