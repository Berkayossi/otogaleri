from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Arac

def anasayfa(request):
    araclar = Arac.objects.all()  # Tüm araçları al
    return render(request, 'galeri/anasayfa.html', {'araclar': araclar})

def araclar_listesi(request):
    # Filtreleme parametreleri
    marka = request.GET.get('marka', '')
    yil_min = request.GET.get('yil_min', '')
    yil_max = request.GET.get('yil_max', '')
    fiyat_min = request.GET.get('fiyat_min', '')
    fiyat_max = request.GET.get('fiyat_max', '')
    durum = request.GET.get('durum', '')
    arama = request.GET.get('arama', '')
    siralama = request.GET.get('siralama', 'ilan_tarihi')  # Varsayılan sıralama
    
    # QuerySet başlat
    araclar = Arac.objects.filter(satildi_mi=False)  # Satılmamış araçlar
    
    # Filtreleme uygula
    if marka:
        araclar = araclar.filter(marka__icontains=marka)
    
    if yil_min:
        araclar = araclar.filter(yil__gte=yil_min)
    
    if yil_max:
        araclar = araclar.filter(yil__lte=yil_max)
    
    if fiyat_min:
        araclar = araclar.filter(fiyat__gte=fiyat_min)
    
    if fiyat_max:
        araclar = araclar.filter(fiyat__lte=fiyat_max)
    
    if durum:
        araclar = araclar.filter(durum=durum)
    
    if arama:
        araclar = araclar.filter(
            Q(marka__icontains=arama) | 
            Q(model__icontains=arama) |
            Q(aciklama__icontains=arama)
        )
    
    # Sıralama uygula
    if siralama == 'fiyat_artan':
        araclar = araclar.order_by('fiyat')
    elif siralama == 'fiyat_azalan':
        araclar = araclar.order_by('-fiyat')
    elif siralama == 'yil_artan':
        araclar = araclar.order_by('yil')
    elif siralama == 'yil_azalan':
        araclar = araclar.order_by('-yil')
    elif siralama == 'marka':
        araclar = araclar.order_by('marka', 'model')
    else:  # ilan_tarihi (varsayılan)
        araclar = araclar.order_by('-ilan_tarihi')
    
    # Sayfalama
    paginator = Paginator(araclar, 12)  # Sayfa başına 12 araç
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Benzersiz markaları al (filtre dropdown için)
    markalar = Arac.objects.values_list('marka', flat=True).distinct().order_by('marka')
    
    context = {
        'page_obj': page_obj,
        'markalar': markalar,
        'current_filters': {
            'marka': marka,
            'yil_min': yil_min,
            'yil_max': yil_max,
            'fiyat_min': fiyat_min,
            'fiyat_max': fiyat_max,
            'durum': durum,
            'arama': arama,
            'siralama': siralama,
        }
    }
    
    return render(request, 'galeri/araclar_listesi.html', context)

def arac_detay(request, arac_id):
    arac = get_object_or_404(Arac, id=arac_id)
    return render(request, 'galeri/arac_detay.html', {'arac': arac})
