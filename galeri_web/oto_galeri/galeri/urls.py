from django.urls import path
from .views import anasayfa, arac_detay, araclar_listesi

urlpatterns = [
    path('', anasayfa, name='anasayfa'),
    path('araclar/', araclar_listesi, name='araclar_listesi'),
    path('arac/<int:arac_id>/', arac_detay, name='arac_detay'),
]
