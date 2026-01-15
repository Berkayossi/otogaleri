from django.contrib import admin
from .models import Arac, ilanDosyalari, Marka, Model

class ilanDosyalariInline(admin.TabularInline):
    model = ilanDosyalari
    extra = 1
    fields = ('fotoğraf', 'sıra', 'ana_fotoğraf')

class AracAdmin(admin.ModelAdmin):
    list_display = ('marka', 'model', 'yil', 'ilan_fiyat', 'durum', 'satildi_mi')
    list_filter = ('durum', 'satildi_mi', 'marka', 'yil')
    search_fields = ('marka__ad', 'model__ad', 'aciklama')
    inlines = [ilanDosyalariInline]

class MarkaAdmin(admin.ModelAdmin):
    list_display = ('ad', 'olusturma_tarihi')
    search_fields = ('ad',)
    ordering = ('ad',)

class ModelAdmin(admin.ModelAdmin):
    list_display = ('ad', 'marka', 'olusturma_tarihi')
    list_filter = ('marka',)
    search_fields = ('ad', 'marka__ad')
    ordering = ('marka', 'ad')

class ilanDosyalariAdmin(admin.ModelAdmin):
    list_display = ('aracid', 'sıra', 'ana_fotoğraf', 'yükleme_tarihi')
    list_filter = ('ana_fotoğraf', 'yükleme_tarihi')
    search_fields = ('aracid__marka__ad', 'aracid__model__ad')

admin.site.register(Marka, MarkaAdmin)
admin.site.register(Model, ModelAdmin)
admin.site.register(Arac, AracAdmin)
admin.site.register(ilanDosyalari, ilanDosyalariAdmin)
