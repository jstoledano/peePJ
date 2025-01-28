from django.urls import path

from .views import (
    SeccionDetailView,
    MunicipioDetailView,
    DistritoDetailView,
    DistritoLocalDetailView,
    DJPDetailView,
    DJCDetailView,
    IndexView
)


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('djc/<int:entidad>/<int:djc>/', DJCDetailView.as_view(), name='djc_detail'),
    path('djp/<int:entidad>/<int:djp>/', DJPDetailView.as_view(), name='djp_detail'),
    path('distrito_local/<int:entidad>/<int:distrito>/', DistritoLocalDetailView.as_view(), name='distrito_local_detail'),
    path('distrito/<int:entidad>/<int:distrito>/', DistritoDetailView.as_view(), name='distrito_detail'),
    path('municipio/<int:entidad>/<int:municipio>/', MunicipioDetailView.as_view(), name='municipio_detail'),
    path('seccion/<int:entidad>/<int:seccion>/', SeccionDetailView.as_view(), name='seccion_detail'),
]