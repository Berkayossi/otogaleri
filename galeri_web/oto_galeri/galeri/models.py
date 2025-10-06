from django.db import models

class Arac(models.Model):
    id = models.AutoField(primary_key=True)
    marka = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    yil = models.IntegerField()
    fiyat = models.IntegerField()
    aciklama = models.TextField()
    durum = models.CharField(max_length=100, choices=[('yeni', 'Yeni'), ('firsat' , 'Fırsat')])
    satildi_mi = models.BooleanField(default=False)
    ilan_tarihi = models.DateTimeField(auto_now_add=True)
    satis_tarihi = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.marka} {self.model} ({self.yil})"
    
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
