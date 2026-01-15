from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from .models import Arac, ilanDosyalari, Marka, Model, personel

def anasayfa(request):
    araclar = Arac.objects.filter(satildi_mi=False)  # Satılmamış araçlar
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
        araclar = araclar.filter(marka__ad__icontains=marka)
    
    if yil_min:
        araclar = araclar.filter(yil__gte=yil_min)
    
    if yil_max:
        araclar = araclar.filter(yil__lte=yil_max)
    
    if fiyat_min:
        araclar = araclar.filter(ilan_fiyat__gte=fiyat_min)
    
    if fiyat_max:
        araclar = araclar.filter(ilan_fiyat__lte=fiyat_max)
    
    if durum:
        araclar = araclar.filter(durum=durum)
    
    if arama:
        araclar = araclar.filter(
            Q(marka__ad__icontains=arama) | 
            Q(model__ad__icontains=arama) |
            Q(aciklama__icontains=arama)
        )
    
    # Sıralama uygula
    if siralama == 'fiyat_artan':
        araclar = araclar.order_by('ilan_fiyat')
    elif siralama == 'fiyat_azalan':
        araclar = araclar.order_by('-ilan_fiyat')
    elif siralama == 'yil_artan':
        araclar = araclar.order_by('yil')
    elif siralama == 'yil_azalan':
        araclar = araclar.order_by('-yil')
    elif siralama == 'marka':
        araclar = araclar.order_by('marka__ad', 'model__ad')
    else:  # ilan_tarihi (varsayılan)
        araclar = araclar.order_by('-ilan_tarihi')
    
    # Sayfalama
    paginator = Paginator(araclar, 12)  # Sayfa başına 12 araç
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Benzersiz markaları al (filtre dropdown için)
    markalar = Marka.objects.all().order_by('ad')
    
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
    
    # Fiyatına yakın araçları bul (+/- %20)
    min_fiyat = arac.ilan_fiyat * 0.7
    max_fiyat = arac.ilan_fiyat * 1.3
    
    benzer_araclar = Arac.objects.filter(
        satildi_mi=False,
        ilan_fiyat__gte=min_fiyat,
        ilan_fiyat__lte=max_fiyat
    ).exclude(id=arac.id).order_by('ilan_fiyat')[:3]
    
    return render(request, 'galeri/arac_detay.html', {'arac': arac, 'benzer_araclar': benzer_araclar})

# Yönetici Panel View'ları
def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Başarıyla giriş yaptınız.')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Kullanıcı adı veya şifre hatalı.')
    
    return render(request, 'galeri/admin/login.html')

@login_required
def admin_logout(request):
    logout(request)
    messages.success(request, 'Başarıyla çıkış yaptınız.')
    return redirect('admin_login')

@login_required
def admin_dashboard(request):
    toplam_arac = Arac.objects.count()
    satilmis_arac = Arac.objects.filter(satildi_mi=True).count()
    satilmamis_arac = Arac.objects.filter(satildi_mi=False).count()
    yeni_arac = Arac.objects.filter(durum='yeni').count()
    firsat_arac = Arac.objects.filter(durum='firsat').count()
    
    son_araclar = Arac.objects.order_by('-ilan_tarihi')[:5]
    
    context = {
        'toplam_arac': toplam_arac,
        'satilmis_arac': satilmis_arac,
        'satilmamis_arac': satilmamis_arac,
        'yeni_arac': yeni_arac,
        'firsat_arac': firsat_arac,
        'son_araclar': son_araclar,
    }
    return render(request, 'galeri/admin/dashboard.html', context)

@login_required
def admin_arac_listesi(request):
    araclar = Arac.objects.all().order_by('-ilan_tarihi')
    paginator = Paginator(araclar, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'galeri/admin/arac_listesi.html', {'page_obj': page_obj})

@login_required
def admin_arac_ekle(request):
    if request.method == 'POST':
        marka_id = request.POST.get('marka_id')
        model_id = request.POST.get('model_id')
        yil = request.POST.get('yil')
        ilan_fiyat = request.POST.get('ilan_fiyat')
        aciklama = request.POST.get('aciklama')
        durum = request.POST.get('durum', 'yeni')
        motor_gucu = request.POST.get('motor_gucu')
        motor_hacmi = request.POST.get('motor_hacmi')
        motor_hacmi = motor_hacmi.replace(',', '.')
        kilometre = request.POST.get('kilometre')
        vites_tipi = request.POST.get('vites_tipi')
        yakit_tipi = request.POST.get('yakit_tipi')
        
        try:
            # Marka ve Model'i al
            if not marka_id:
                messages.error(request, 'Marka seçimi zorunludur.')
                context = {
                    'markalar': Marka.objects.all().order_by('ad'),
                }
                return render(request, 'galeri/admin/arac_ekle.html', context)
            
            marka = get_object_or_404(Marka, id=marka_id)
            
            if not model_id:
                messages.error(request, 'Model seçimi zorunludur.')
                context = {
                    'markalar': Marka.objects.all().order_by('ad'),
                }
                return render(request, 'galeri/admin/arac_ekle.html', context)
            
            model = get_object_or_404(Model, id=model_id, marka=marka)
            
            # Alış fiyatı (opsiyonel)
            alis_fiyat_str = request.POST.get('alis_fiyat', '').strip()
            alis_fiyat = int(alis_fiyat_str) if alis_fiyat_str else None
            
            # Satış fiyatı (opsiyonel)
            satis_fiyat_str = request.POST.get('satis_fiyat', '').strip()
            satis_fiyat = int(satis_fiyat_str) if satis_fiyat_str else None
            
            # Kar/Zarar hesaplama
            kar_zarar = None
            satis_tarihi = None
            if satis_fiyat is not None:
                # Eğer alış fiyatı varsa: Kar = Satış Fiyatı - Alış Fiyatı
                # Eğer alış fiyatı yoksa: Kar = Satış Fiyatı - İlan Fiyatı
                if alis_fiyat is not None:
                    kar_zarar = satis_fiyat - alis_fiyat
                else:
                    kar_zarar = satis_fiyat - int(ilan_fiyat)
                
                # Eğer satıldı olarak işaretlenmişse, satış tarihini kaydet
                satildi_mi = request.POST.get('satildi_mi') == 'on'
                if satildi_mi:
                    from django.utils import timezone
                    satis_tarihi = timezone.now()
            
            arac = Arac.objects.create(
                marka=marka,
                model=model,
                yil=int(yil),
                ilan_fiyat=int(ilan_fiyat),
                alis_fiyat=alis_fiyat,
                motor_gucu=motor_gucu,
                motor_hacmi=motor_hacmi,
                kilometre=kilometre,
                vites_tipi=vites_tipi,
                yakit_tipi=yakit_tipi,
                satis_fiyat=satis_fiyat,
                kar_zarar=kar_zarar,
                satis_tarihi=satis_tarihi,
                aciklama=aciklama,
                durum=durum,
                satildi_mi=request.POST.get('satildi_mi') == 'on' if satis_fiyat else False,
                personel=get_object_or_404(personel, id=request.POST.get('personel')) if request.POST.get('personel') else None
            )
            
            # Fotoğrafları işle
            if 'fotograflar' in request.FILES:
                fotograflar = request.FILES.getlist('fotograflar')
                for idx, foto in enumerate(fotograflar, start=1):
                    ana_foto = (idx == 1)  # İlk fotoğraf ana fotoğraf
                    ilanDosyalari.objects.create(
                        aracid=arac,
                        fotoğraf=foto,
                        sıra=idx,
                        ana_fotoğraf=ana_foto
                    )
            
            messages.success(request, f'{arac.marka.ad} {arac.model.ad} başarıyla eklendi.')
            return redirect('admin_arac_listesi')
        except Exception as e:
            messages.error(request, f'Hata: {str(e)}')
    
    context = {
        'markalar': Marka.objects.all().order_by('ad'),
        'personeller': personel.objects.all().order_by('ad'),
    }
    return render(request, 'galeri/admin/arac_ekle.html', context)

@login_required
def admin_arac_duzenle(request, arac_id):
    arac = get_object_or_404(Arac, id=arac_id)
    fotograflar = arac.fotograflar.all()
    
    if request.method == 'POST':
        try:
            marka_id = request.POST.get('marka_id')
            model_id = request.POST.get('model_id')
            yil = request.POST.get('yil', '')
            ilan_fiyat = request.POST.get('ilan_fiyat', '')
            personel_id = request.POST.get('personel_id')
            motor_gucu = request.POST.get('motor_gucu', '')
            motor_hacmi = request.POST.get('motor_hacmi', '')
            motor_hacmi = motor_hacmi.replace(',', '.')
            kilometre = request.POST.get('kilometre', '')
            vites_tipi = request.POST.get('vites_tipi', '')
            yakit_tipi = request.POST.get('yakit_tipi', '')
            
            if not yil or not ilan_fiyat:
                messages.error(request, 'Yıl ve fiyat alanları zorunludur.')
                context = {
                    'arac': arac,
                    'fotograflar': fotograflar,
                    'markalar': Marka.objects.all().order_by('ad'),
                    'modeller': Model.objects.filter(marka=arac.marka).order_by('ad'),
                }
                return render(request, 'galeri/admin/arac_duzenle.html', context)
            
            # Marka ve Model'i al
            if marka_id:
                arac.marka = get_object_or_404(Marka, id=marka_id)
            
            if model_id:
                arac.model = get_object_or_404(Model, id=model_id, marka=arac.marka)
            
            # Personel ataması
            personel_id_debug = request.POST.get('personel_id')
            print(f"DEBUG: personel_id = '{personel_id_debug}', type = {type(personel_id_debug)}")
            
            if personel_id and personel_id.strip():
                arac.personel = get_object_or_404(personel, id=personel_id)
                print(f"DEBUG: Personel atandı: {arac.personel}")
            else:
                arac.personel = None
                print("DEBUG: Personel None olarak ayarlandı")
            
            arac.yil = int(yil)
            arac.ilan_fiyat = int(ilan_fiyat)
            arac.motor_gucu = int(motor_gucu)
            arac.motor_hacmi = float(motor_hacmi)
            arac.kilometre = int(kilometre)
            arac.vites_tipi = vites_tipi
            arac.yakit_tipi = yakit_tipi
            arac.aciklama = request.POST.get('aciklama', '').strip()
            arac.durum = request.POST.get('durum', 'yeni')
            arac.satildi_mi = request.POST.get('satildi_mi') == 'on'
            
            # Alış fiyatı (opsiyonel)
            alis_fiyat_str = request.POST.get('alis_fiyat', '').strip()
            if alis_fiyat_str:
                arac.alis_fiyat = int(alis_fiyat_str)
            else:
                arac.alis_fiyat = None
            
            # Satış fiyatı (opsiyonel)
            satis_fiyat_str = request.POST.get('satis_fiyat', '').strip()
            if satis_fiyat_str:
                arac.satis_fiyat = int(satis_fiyat_str)
            else:
                arac.satis_fiyat = None
            
            # Kar/Zarar hesaplama
            if arac.satis_fiyat is not None:
                # Eğer alış fiyatı varsa: Kar = Satış Fiyatı - Alış Fiyatı
                # Eğer alış fiyatı yoksa: Kar = Satış Fiyatı - İlan Fiyatı
                if arac.alis_fiyat is not None:
                    arac.kar_zarar = arac.satis_fiyat - arac.alis_fiyat
                else:
                    arac.kar_zarar = arac.satis_fiyat - arac.ilan_fiyat
                
                # Eğer satıldı olarak işaretlenmişse ve satış tarihi yoksa, şimdiki zamanı kaydet
                if arac.satildi_mi and not arac.satis_tarihi:
                    from django.utils import timezone
                    arac.satis_tarihi = timezone.now()
            else:
                # Satış fiyatı yoksa kar/zarar da null
                arac.kar_zarar = None
                # Eğer satıldı işareti kaldırıldıysa satış tarihini de temizle
                if not arac.satildi_mi:
                    arac.satis_tarihi = None
            
            arac.save()
            
            # Yeni fotoğraflar ekle
            if 'fotograflar' in request.FILES:
                mevcut_sira = fotograflar.count()
                yeni_fotograflar = request.FILES.getlist('fotograflar')
                for idx, foto in enumerate(yeni_fotograflar, start=mevcut_sira + 1):
                    ilanDosyalari.objects.create(
                        aracid=arac,
                        fotoğraf=foto,
                        sıra=idx,
                        ana_fotoğraf=False
                    )
            
            # Ana fotoğraf güncelle
            ana_foto_id = request.POST.get('ana_foto')
            if ana_foto_id:
                ilanDosyalari.objects.filter(aracid=arac).update(ana_fotoğraf=False)
                ilanDosyalari.objects.filter(id=ana_foto_id).update(ana_fotoğraf=True)
            
            messages.success(request, f'{arac.marka.ad} {arac.model.ad} başarıyla güncellendi.')
            return redirect('admin_arac_listesi')
        except ValueError as e:
            messages.error(request, f'Hata: Geçersiz sayısal değer. {str(e)}')
        except Exception as e:
            messages.error(request, f'Hata oluştu: {str(e)}')
    
    context = {
        'arac': arac,
        'fotograflar': fotograflar,
        'markalar': Marka.objects.all().order_by('ad'),
        'modeller': Model.objects.filter(marka=arac.marka).order_by('ad'),
        'personeller': personel.objects.all().order_by('ad'),
    }
    return render(request, 'galeri/admin/arac_duzenle.html', context)

@login_required
def admin_arac_sil(request, arac_id):
    arac = get_object_or_404(Arac, id=arac_id)
    if request.method == 'POST':
        arac_adi = f'{arac.marka.ad} {arac.model.ad}'
        arac.delete()
        messages.success(request, f'{arac_adi} başarıyla silindi.')
        return redirect('admin_arac_listesi')
    return render(request, 'galeri/admin/arac_sil.html', {'arac': arac})

@login_required
def admin_foto_sil(request, foto_id):
    foto = get_object_or_404(ilanDosyalari, id=foto_id)
    if request.method == 'POST':
        foto.delete()
        messages.success(request, 'Fotoğraf başarıyla silindi.')
        return redirect('admin_arac_duzenle', arac_id=foto.aracid.id)
    return JsonResponse({'success': False})

@login_required
def admin_personel_listesi(request):
    personeller = personel.objects.all().order_by('ad')
    paginator = Paginator(personeller, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'galeri/admin/personel_listesi.html', {'page_obj': page_obj})

@login_required
def admin_personel_ekle(request):
    if request.method == 'POST':
        ad = request.POST.get('ad')
        soyad = request.POST.get('soyad')
        telefon = request.POST.get('telefon')
        e_posta = request.POST.get('e_posta')
        
        try:
            if not ad or not soyad:
                messages.error(request, 'Ad ve Soyad alanları zorunludur.')
                return render(request, 'galeri/admin/personel_ekle.html')
            
            p = personel.objects.create(
                ad=ad,
                soyad=soyad,
                telefon=telefon,
                e_posta=e_posta
            )
            
            messages.success(request, f'{p.ad} {p.soyad} başarıyla eklendi.')
            return redirect('admin_personel_listesi')
        except Exception as e:
            messages.error(request, f'Hata: {str(e)}')
    
    return render(request, 'galeri/admin/personel_ekle.html')

@login_required
def admin_personel_duzenle(request, personel_id):
    p = get_object_or_404(personel, id=personel_id)
    
    if request.method == 'POST':
        try:
            p.ad = request.POST.get('ad')
            p.soyad = request.POST.get('soyad')
            p.telefon = request.POST.get('telefon')
            p.e_posta = request.POST.get('e_posta')
            
            if not p.ad or not p.soyad:
                messages.error(request, 'Ad ve Soyad alanları zorunludur.')
                return render(request, 'galeri/admin/personel_duzenle.html', {'personel': p})
            
            p.save()
            messages.success(request, f'{p.ad} {p.soyad} başarıyla güncellendi.')
            return redirect('admin_personel_listesi')
        except Exception as e:
            messages.error(request, f'Hata: {str(e)}')
    
    return render(request, 'galeri/admin/personel_duzenle.html', {'personel': p})

@login_required
def admin_personel_sil(request, personel_id):
    p = get_object_or_404(personel, id=personel_id)
    if request.method == 'POST':
        # Personelin araçlarla ilişkisi varsa protekli olduğu için silinemeyebilir
        # Ancak models.py'da on_delete=models.PROTECT olduğu için Django otomatik hata verecektir.
        # Bunu try-catch ile yakalamak daha şık olur ama şimdilik standart akışta yapalım.
        try:
            ad_soyad = f'{p.ad} {p.soyad}'
            p.delete()
            messages.success(request, f'{ad_soyad} başarıyla silindi.')
        except Exception as e:
             messages.error(request, f'Silinemedi. Bu personele atanmış araçlar olabilir. Hata: {str(e)}')
        return redirect('admin_personel_listesi')
    return render(request, 'galeri/admin/personel_sil.html', {'personel': p})

# API Endpoints
def get_modeller_by_marka(request, marka_id):
    """Belirli bir markaya ait modelleri JSON olarak döndürür"""
    try:
        marka = get_object_or_404(Marka, id=marka_id)
        modeller = Model.objects.filter(marka=marka).order_by('ad')
        
        modeller_list = [
            {
                'id': model.id,
                'ad': model.ad
            }
            for model in modeller
        ]
        
        return JsonResponse({
            'success': True,
            'modeller': modeller_list
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
