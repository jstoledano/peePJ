from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('peepj/', include('gis.urls')),
    path('admin/', admin.site.urls),
]
