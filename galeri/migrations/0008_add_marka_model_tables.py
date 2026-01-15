# Generated manually

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('galeri', '0007_rename_fiyat_arac_ilan_fiyat_arac_alis_fiyat_and_more'),
    ]

    operations = [
        # Önce Marka tablosunu oluştur
        migrations.CreateModel(
            name='Marka',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ad', models.CharField(max_length=100, unique=True)),
                ('olusturma_tarihi', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Marka',
                'verbose_name_plural': 'Markalar',
                'ordering': ['ad'],
            },
        ),
        # Model tablosunu oluştur
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ad', models.CharField(max_length=100)),
                ('olusturma_tarihi', models.DateTimeField(auto_now_add=True)),
                ('marka', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modeller', to='galeri.marka')),
            ],
            options={
                'verbose_name': 'Model',
                'verbose_name_plural': 'Modeller',
                'ordering': ['marka', 'ad'],
                'unique_together': {('marka', 'ad')},
            },
        ),
        # Arac tablosuna geçici sütunlar ekle (ForeignKey'ler) - null=True çünkü henüz veri yok
        migrations.AddField(
            model_name='arac',
            name='marka_temp',
            field=models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='araclar_temp', to='galeri.marka'),
        ),
        migrations.AddField(
            model_name='arac',
            name='model_temp',
            field=models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='araclar_temp', to='galeri.model'),
        ),
    ]

