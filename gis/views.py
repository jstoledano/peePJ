from django.views.generic import DetailView
from .models import (
    Seccion,
    Municipio,
    DistritoFederal,
    DistritoLocal,
    DJP
)


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


class DistritoDetailView(DetailView):
    model = DistritoFederal
    context_object_name = 'distrito'

    def get_object(self):
        entidad = self.kwargs.get("entidad")
        distrito = self.kwargs.get("distrito")
        return DistritoFederal.objects.get(entidad__entidad=entidad, distrito_federal=distrito)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        secciones = Seccion.objects.filter(distrito_federal=self.get_object())
        secciones_por_municipio = {}
        for seccion in secciones:
            municipio = seccion.municipio
            if municipio not in secciones_por_municipio:
                secciones_por_municipio[municipio] = []
            secciones_por_municipio[municipio].append(seccion)
        context['secciones_por_municipio'] = secciones_por_municipio
        return context


class DistritoLocalDetailView(DetailView):
    model = DistritoLocal
    context_object_name = 'distrito'

    def get_object(self):
        entidad = self.kwargs.get("entidad")
        distrito = self.kwargs.get("distrito")
        return DistritoLocal.objects.get(entidad__entidad=entidad, distrito_local=distrito)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        secciones = Seccion.objects.filter(distrito_local=self.get_object())
        secciones_por_municipio = {}
        for seccion in secciones:
            municipio = seccion.municipio
            if municipio not in secciones_por_municipio:
                secciones_por_municipio[municipio] = []
            secciones_por_municipio[municipio].append(seccion)
        context['secciones_por_municipio'] = secciones_por_municipio
        return context


class DJPDetailView(DetailView):
    model = DJP
    context_object_name = 'djp'

    def get_object(self):
        entidad = self.kwargs.get("entidad")
        djp = self.kwargs.get("djp")
        return DJP.objects.get(entidad__entidad=entidad, djp=djp)