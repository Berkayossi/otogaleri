from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from galeri.models import Arac, personel


class Command(BaseCommand):
    help = 'Django Groups ve Permissions oluşturur'

    def handle(self, *args, **options):
        # Admin Grubu
        admin_group, created = Group.objects.get_or_create(name='Admin')
        if created:
            self.stdout.write(self.style.SUCCESS('Admin grubu oluşturuldu.'))
        else:
            self.stdout.write('Admin grubu zaten mevcut.')

        # Rapor Görüntüleyici Grubu
        rapor_group, created = Group.objects.get_or_create(name='Rapor Görüntüleyici')
        if created:
            self.stdout.write(self.style.SUCCESS('Rapor Görüntüleyici grubu oluşturuldu.'))
        else:
            self.stdout.write('Rapor Görüntüleyici grubu zaten mevcut.')

        # Araç Yöneticisi Grubu
        arac_yoneticisi_group, created = Group.objects.get_or_create(name='Araç Yöneticisi')
        if created:
            self.stdout.write(self.style.SUCCESS('Araç Yöneticisi grubu oluşturuldu.'))
        else:
            self.stdout.write('Araç Yöneticisi grubu zaten mevcut.')

        # İsteğe bağlı: Permission'ları gruplara atayabilirsiniz
        # Örnek: Admin grubuna tüm Arac ve personel permission'larını ver
        try:
            arac_content_type = ContentType.objects.get_for_model(Arac)
            personel_content_type = ContentType.objects.get_for_model(personel)
            
            # Admin grubuna tüm permission'ları ekle
            admin_permissions = Permission.objects.filter(
                content_type__in=[arac_content_type, personel_content_type]
            )
            admin_group.permissions.set(admin_permissions)
            self.stdout.write(self.style.SUCCESS(f'Admin grubuna {admin_permissions.count()} permission eklendi.'))
            
            # Araç Yöneticisi grubuna sadece Arac permission'larını ekle (ekleme, düzenleme, silme)
            arac_permissions = Permission.objects.filter(
                content_type=arac_content_type,
                codename__in=['add_arac', 'change_arac', 'delete_arac', 'view_arac']
            )
            arac_yoneticisi_group.permissions.set(arac_permissions)
            self.stdout.write(self.style.SUCCESS(f'Araç Yöneticisi grubuna {arac_permissions.count()} permission eklendi.'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Permission atama hatası: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('\nGruplar başarıyla oluşturuldu!'))
        self.stdout.write('\nKullanım:')
        self.stdout.write('1. Django admin panelinden veya kullanıcı yönetimi sayfasından kullanıcıları gruplara atayın.')
        self.stdout.write('2. Superuser: Tüm yetkilere sahip')
        self.stdout.write('3. Admin grubu: Araç ve personel yönetimi')
        self.stdout.write('4. Rapor Görüntüleyici grubu: Sadece rapor görüntüleme')
        self.stdout.write('5. Araç Yöneticisi grubu: Araç ekleme, düzenleme ve silme yetkisi')