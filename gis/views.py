from django.views.generic import DetailView
from .models import Seccion, Municipio


class SeccionDetailView(DetailView):
    model = Seccion
    context_object_name = 'seccion'

    def get_object(self):
        entidad = self.kwargs.get("entidad")
        seccion = self.kwargs.get("seccion")
        return Seccion.objects.get(entidad__entidad=entidad, seccion=seccion)

class MunicipioDetailView(DetailView):
    model = Municipio
    context_object_name = 'municipio'

    def get_object(self):
        entidad = self.kwargs.get("entidad")
        municipio = self.kwargs.get("municipio")
        return Municipio.objects.get(entidad__entidad=entidad, municipio=municipio)