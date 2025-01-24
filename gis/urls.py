from django.urls import path
from .views import (
    SeccionDetailView,
    MunicipioDetailView
)


urlpatterns = [
    path('municipio/<int:entidad>/<int:municipio>/', MunicipioDetailView.as_view(), name='municipio_detail'),
    path('seccion/<int:entidad>/<int:seccion>/', SeccionDetailView.as_view(), name='seccion_detail'),
]