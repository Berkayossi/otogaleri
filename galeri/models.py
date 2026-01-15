from django.db import models

class Marka(models.Model):
    id = models.AutoField(primary_key=True)
    ad = models.CharField(max_length=100, unique=True)
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['ad']
        verbose_name = "Marka"
        verbose_name_plural = "Markalar"
    
    def __str__(self):
        return self.ad

class Model(models.Model):
    id = models.AutoField(primary_key=True)
    marka = models.ForeignKey(Marka, on_delete=models.CASCADE, related_name='modeller')
    ad = models.CharField(max_length=100)
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['marka', 'ad']
        unique_together = ['marka', 'ad']
        verbose_name = "Model"
        verbose_name_plural = "Modeller"
    
    def __str__(self):
        return f"{self.marka.ad} {self.ad}"

class Arac(models.Model):
    id = models.AutoField(primary_key=True)
    marka = models.ForeignKey(Marka, on_delete=models.PROTECT, related_name='araclar')
    model = models.ForeignKey(Model, on_delete=models.PROTECT, related_name='araclar')
    yil = models.IntegerField()
    ilan_fiyat = models.IntegerField()
    satis_fiyat = models.IntegerField(null=True, blank=True)
    alis_fiyat = models.IntegerField(null=True, blank=True)
    kar_zarar = models.IntegerField(null=True, blank=True)
    aciklama = models.TextField()
    durum = models.CharField(max_length=100, choices=[('yeni', 'Yeni'), ('firsat', 'Fırsat')])
    satildi_mi = models.BooleanField(default=False)
    ilan_tarihi = models.DateTimeField(auto_now_add=True)
    satis_tarihi = models.DateTimeField(null=True, blank=True)
    personel = models.ForeignKey('personel', on_delete=models.PROTECT, related_name='araclar', null=True, blank=True)
    kilometre = models.IntegerField(null=True, blank=True, default=0)
    vites_tipi = models.CharField(max_length=100, choices=[('manuel', 'Manuel'), ('otomatik', 'Otomatik')], null=True, blank=True)
    yakit_tipi = models.CharField(max_length=100, choices=[('benzin', 'Benzin'), ('dizel', 'Dizel'), ('elektrik', 'Elektrik')], null=True, blank=True)
    motor_gucu = models.IntegerField(null=True, blank=True, default=0)
    motor_hacmi = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True, default=0)

    def __str__(self):
        return f"{self.marka.ad} {self.model.ad} ({self.yil})"
    
    @property
    def ana_fotoğraf(self):
        """Ana fotoğrafı işaretlenmiş olanı döndür, yoksa ilk fotoğrafı döndür"""
        ana_foto = self.fotograflar.filter(ana_fotoğraf=True).first()
        return ana_foto or self.fotograflar.first()
    
    def get_ana_foto_url(self):
        """Ana fotoğrafın URL'sini döndür"""
        ana_foto = self.ana_fotoğraf
        return ana_foto.fotoğraf.url if ana_foto else None

class ilanDosyalari(models.Model):
    aracid = models.ForeignKey(Arac, on_delete=models.CASCADE, related_name='fotograflar')
    fotoğraf = models.ImageField(upload_to='araclar/')
    sıra = models.PositiveIntegerField(default=1, help_text="Fotoğraf sırası")
    ana_fotoğraf = models.BooleanField(default=False, help_text="Ana fotoğraf olarak işaretle")
    yükleme_tarihi = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sıra', 'yükleme_tarihi']
        verbose_name = "Araç Fotoğrafı"
        verbose_name_plural = "Araç Fotoğrafları"

    def __str__(self):
        return f"{self.aracid} - Fotoğraf {self.sıra}"

class personel(models.Model):
    id = models.AutoField(primary_key=True)
    ad = models.CharField(max_length=100)
    soyad = models.CharField(max_length=100)
    telefon = models.CharField(max_length=20)
    e_posta = models.EmailField()
    