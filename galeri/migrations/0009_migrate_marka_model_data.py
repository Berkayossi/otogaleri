# Generated manually - Veri migrasyonu

from django.db import migrations


def migrate_marka_model_data(apps, schema_editor):
    """Mevcut marka ve model verilerini yeni tablolara taşı"""
    Arac = apps.get_model('galeri', 'Arac')
    Marka = apps.get_model('galeri', 'Marka')
    Model = apps.get_model('galeri', 'Model')
    
    # Tüm araçları al
    araclar = Arac.objects.all()
    
    # Benzersiz marka ve model kombinasyonlarını bul
    marka_model_dict = {}
    
    for arac in araclar:
        marka_ad = arac.marka  # Eski CharField
        model_ad = arac.model  # Eski CharField
        
        # Marka oluştur veya al
        marka, created = Marka.objects.get_or_create(ad=marka_ad)
        
        # Model oluştur veya al
        model, created = Model.objects.get_or_create(marka=marka, ad=model_ad)
        
        # Geçici ForeignKey'leri güncelle
        arac.marka_temp = marka
        arac.model_temp = model
        arac.save()


def reverse_migrate(apps, schema_editor):
    """Geri alma işlemi - gerekirse"""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('galeri', '0008_add_marka_model_tables'),
    ]

    operations = [
        migrations.RunPython(migrate_marka_model_data, reverse_migrate),
    ]

