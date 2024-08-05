from django.contrib import admin
from .models import *

# Register your models here.
# admin.site.register(Movie)
# admin.site.register(Actor)


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'photo')


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('isim', 'resim', 'video', 'kategori')
    filter_horizontal = ('actors',)


@admin.register(Yorum)
class YorumAdmin(admin.ModelAdmin):
    list_display = ('user', 'film', 'rating', 'created_at')


@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
    list_display = ('isim',)