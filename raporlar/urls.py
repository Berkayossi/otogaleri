from django.urls import path
from . import views

app_name = 'raporlar'

urlpatterns = [
    path('', views.raporlar, name='raporlar'),
    path('pdf/', views.rapor_pdf, name='rapor_pdf'),
    path('excel/', views.rapor_excel, name='rapor_excel'),
]

