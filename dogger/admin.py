from django.contrib import admin
from .models import Dog, DogSize


# Register your models here.
@admin.register(DogSize)
class DogSizeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'label',)
    link_display_links = ('pk', 'label')

    search_fields = ('label',)


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'size', 'owner',)
    link_display_links = ('pk', 'name')

    search_fields = ('name',)

    list_filter = ('owner',)
