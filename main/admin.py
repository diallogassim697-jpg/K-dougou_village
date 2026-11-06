from django.contrib import admin
from .models import Article, Evenement, ImageEvenement

admin.site.register(Article)


class ImageEvenementInline(admin.TabularInline):
    model = ImageEvenement
    extra = 3
    verbose_name = "image"
    verbose_name_plural = "Images de l'événement"


@admin.register(Evenement)
class EvenementAdmin(admin.ModelAdmin):
    list_display = ("titre", "date_heure", "lieu")
    list_filter = ("date_heure",)
    search_fields = ("titre", "description", "lieu")
    inlines = [ImageEvenementInline]
