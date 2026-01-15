from django.urls import path
from .views import (
    anasayfa, arac_detay, araclar_listesi,
    admin_login, admin_logout, admin_dashboard,
    admin_arac_listesi, admin_arac_ekle, admin_arac_duzenle,
    admin_arac_sil, admin_foto_sil, get_modeller_by_marka,
    admin_personel_listesi, admin_personel_ekle, admin_personel_duzenle, admin_personel_sil
)

urlpatterns = [
    path('', anasayfa, name='anasayfa'),
    path('araclar/', araclar_listesi, name='araclar_listesi'),
    path('arac/<int:arac_id>/', arac_detay, name='arac_detay'),
    
    # Yönetici Panel URL'leri
    path('yonetim/giris/', admin_login, name='admin_login'),
    path('yonetim/cikis/', admin_logout, name='admin_logout'),
    path('yonetim/', admin_dashboard, name='admin_dashboard'),
    path('yonetim/araclar/', admin_arac_listesi, name='admin_arac_listesi'),
    path('yonetim/arac/ekle/', admin_arac_ekle, name='admin_arac_ekle'),
    path('yonetim/arac/<int:arac_id>/duzenle/', admin_arac_duzenle, name='admin_arac_duzenle'),
    path('yonetim/arac/<int:arac_id>/sil/', admin_arac_sil, name='admin_arac_sil'),
    path('yonetim/foto/<int:foto_id>/sil/', admin_foto_sil, name='admin_foto_sil'),
    
    # Personel Yönetimi
    path('yonetim/personel/', admin_personel_listesi, name='admin_personel_listesi'),
    path('yonetim/personel/ekle/', admin_personel_ekle, name='admin_personel_ekle'),
    path('yonetim/personel/<int:personel_id>/duzenle/', admin_personel_duzenle, name='admin_personel_duzenle'),
    path('yonetim/personel/<int:personel_id>/sil/', admin_personel_sil, name='admin_personel_sil'),
    
    # API Endpoints
    path('api/modeller/<int:marka_id>/', get_modeller_by_marka, name='get_modeller_by_marka'),
]
