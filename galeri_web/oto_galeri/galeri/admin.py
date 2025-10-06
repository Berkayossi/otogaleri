from django.contrib import admin
from .models import Arac, ilanDosyalari

class ilanDosyalariInline(admin.TabularInline):
    model = ilanDosyalari
    extra = 1
    fields = ('fotoğraf', 'sıra', 'ana_fotoğraf')

class AracAdmin(admin.ModelAdmin):
    list_display = ('marka', 'model', 'yil', 'fiyat', 'durum', 'satildi_mi')
    list_filter = ('durum', 'satildi_mi', 'marka', 'yil')
    search_fields = ('marka', 'model', 'aciklama')
    inlines = [ilanDosyalariInline]

class ilanDosyalariAdmin(admin.ModelAdmin):
    list_display = ('aracid', 'sıra', 'ana_fotoğraf', 'yükleme_tarihi')
    list_filter = ('ana_fotoğraf', 'yükleme_tarihi')
    search_fields = ('aracid__marka', 'aracid__model')

admin.site.register(Arac, AracAdmin)
admin.site.register(ilanDosyalari, ilanDosyalariAdmin)
