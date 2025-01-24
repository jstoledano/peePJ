from django.contrib import admin
from gis.models import (
    Entidad,
    DistritoFederal,
    DistritoLocal,
    DJP,
    DJC,
    Municipio,
    Seccion,
    ZORE,HistoricoPE
)


admin.site.register(Entidad)
admin.site.register(DistritoFederal)
admin.site.register(DistritoLocal)
admin.site.register(DJP)
admin.site.register(DJC)
admin.site.register(Municipio)
admin.site.register(Seccion)
admin.site.register(HistoricoPE)
