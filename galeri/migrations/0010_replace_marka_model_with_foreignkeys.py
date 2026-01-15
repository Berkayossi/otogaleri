# Generated manually - ForeignKey'e geçiş

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('galeri', '0009_migrate_marka_model_data'),
    ]

    operations = [
        # Eski CharField sütunlarını sil
        migrations.RemoveField(
            model_name='arac',
            name='marka',
        ),
        migrations.RemoveField(
            model_name='arac',
            name='model',
        ),
        # Geçici ForeignKey'leri kalıcı yap ve yeniden adlandır
        migrations.RenameField(
            model_name='arac',
            old_name='marka_temp',
            new_name='marka',
        ),
        migrations.RenameField(
            model_name='arac',
            old_name='model_temp',
            new_name='model',
        ),
        # ForeignKey'leri null=False yap
        migrations.AlterField(
            model_name='arac',
            name='marka',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='araclar', to='galeri.marka'),
        ),
        migrations.AlterField(
            model_name='arac',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='araclar', to='galeri.model'),
        ),
        # Durum alanını güncelle (blank=True kaldır)
        migrations.AlterField(
            model_name='arac',
            name='durum',
            field=models.CharField(choices=[('yeni', 'Yeni'), ('firsat', 'Fırsat')], max_length=100),
        ),
    ]

