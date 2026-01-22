from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def admin_required(view_func):
    """
    Kullanıcının admin yetkisine sahip olmasını gerektirir.
    Superuser veya 'Admin' grubunda olan kullanıcılar erişebilir.
    """
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser or request.user.groups.filter(name='Admin').exists():
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'Bu sayfaya erişim yetkiniz bulunmamaktadır.')
            return redirect('admin_login')
    return _wrapped_view


def rapor_required(view_func):
    """
    Kullanıcının rapor görüntüleme yetkisine sahip olmasını gerektirir.
    Superuser, 'Admin' veya 'Rapor Görüntüleyici' grubunda olan kullanıcılar erişebilir.
    """
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if (request.user.is_superuser or 
            request.user.groups.filter(name__in=['Admin', 'Rapor Görüntüleyici']).exists()):
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'Rapor görüntüleme yetkiniz bulunmamaktadır.')
            return redirect('admin_login')
    return _wrapped_view


def superuser_required(view_func):
    """
    Sadece superuser'ların erişebileceği view'lar için.
    Kullanıcı yönetimi gibi kritik işlemler için kullanılır.
    """
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'Bu işlem için superuser yetkisi gereklidir.')
            return redirect('admin_login')
    return _wrapped_view


def arac_yoneticisi_required(view_func):
    """
    Araç ekleme, silme ve düzenleme yetkisi için.
    Superuser, 'Admin' veya 'Araç Yöneticisi' grubunda olan kullanıcılar erişebilir.
    """
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if (request.user.is_superuser or 
            request.user.groups.filter(name__in=['Admin', 'Araç Yöneticisi']).exists()):
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'Araç yönetimi için yetkiniz bulunmamaktadır.')
            return redirect('admin_login')
    return _wrapped_view
