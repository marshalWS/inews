from django.contrib import admin

# Register your models here.
from .models import news,writer,video

class FileInline(admin.StackedInline):
    model = video
    extra = 3
class newsAdmin(admin.ModelAdmin):
    model=news
    inlines = [FileInline]

admin.site.register(news,newsAdmin)
admin.site.register(writer)