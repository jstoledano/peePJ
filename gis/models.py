from django.utils import timezone
from django.db import models


TIPO_SECCION = (
    (2, 'URBANA'),
    (3, 'MIXTA'),
    (4, 'RURAL')
)


class Entidad(models.Model):
    entidad = models.PositiveSmallIntegerField()
    nombre = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Entidades"
        ordering = ['entidad']

    def __str__(self):
        return f"{self.entidad:02d} - {self.nombre.upper()}"

    def get_padron(self):
        return sum(municipio.get_padron() for municipio in self.municipio_set.all())

    def get_lista_nominal(self):
        return sum(municipio.get_lista_nominal() for municipio in self.municipio_set.all())

    def get_fecha_corte(self):
        latest_estadistico = EstadisticoSeccion.objects.filter(entidad=self).latest('historico__fecha')
        return latest_estadistico.historico.fecha if latest_estadistico else None


class DistritoFederal(models.Model):
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)
    distrito_federal = models.PositiveSmallIntegerField("Distrito")

    class Meta:
        verbose_name = "Distrito"
        verbose_name_plural = "Distritos"
        ordering = ['entidad', 'distrito_federal']

    def __str__(self):
        return f"{self.entidad.entidad:02d} - {self.distrito_federal:02d}"

    def get_padron(self):
        return sum(seccion.get_padron() for seccion in self.seccion_set.all())

    def get_lista_nominal(self):
        return sum(seccion.get_lista_nominal() for seccion in self.seccion_set.all())

    def get_fecha_corte(self):
        latest_estadistico = EstadisticoSeccion.objects.filter(seccion__distrito_federal=self).latest('historico__fecha')
        return latest_estadistico.historico.fecha if latest_estadistico else None


class DistritoLocal(models.Model):
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)
    distrito_local = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = "Distrito Local"
        verbose_name_plural = "Distritos Locales"
        ordering = ['entidad', 'distrito_local']

    def __str__(self):
        return f"{self.entidad.entidad:02d} - {self.distrito_local:02d}"

    def get_padron(self):
        return sum(seccion.get_padron() for seccion in self.seccion_set.all())

    def get_lista_nominal(self):
        return sum(seccion.get_lista_nominal() for seccion in self.seccion_set.all())

    def get_fecha_corte(self):
        latest_estadistico = EstadisticoSeccion.objects.filter(seccion__distrito_local=self).latest('historico__fecha')
        return latest_estadistico.historico.fecha if latest_estadistico else None


class DJP(models.Model):
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)
    djp = models.PositiveSmallIntegerField("DJP")
    nombre = models.CharField(max_length=100)

    class Meta:
        verbose_name = "DJP"
        verbose_name_plural = "Distritos Judiciales Penales"
        ordering = ['entidad', 'djp']

    def __str__(self):
        return f"{self.nombre}"

    def get_padron(self):
        return sum(municipio.get_padron() for municipio in self.municipio_set.all())

    def get_lista_nominal(self):
        return sum(municipio.get_lista_nominal() for municipio in self.municipio_set.all())

    def get_fecha_corte(self):
        latest_estadistico = EstadisticoSeccion.objects.filter(seccion__municipio__djp=self).latest('historico__fecha')
        return latest_estadistico.historico.fecha if latest_estadistico else None


class DJC(models.Model):
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)
    djc = models.PositiveSmallIntegerField("DJC")
    nombre = models.CharField(max_length=100)

    class Meta:
        verbose_name = "DJC"
        verbose_name_plural = "Distritos Judiciales Civiles"
        ordering = ['entidad', 'djc']

    def __str__(self):
        return f"{self.nombre}"

    def get_padron(self):
        return sum(municipio.get_padron() for municipio in self.municipio_set.all())

    def get_lista_nominal(self):
        return sum(municipio.get_lista_nominal() for municipio in self.municipio_set.all())

    def get_fecha_corte(self):
        latest_estadistico = EstadisticoSeccion.objects.filter(seccion__municipio__djc=self).latest('historico__fecha')
        return latest_estadistico.historico.fecha if latest_estadistico else None


class Municipio(models.Model):
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)
    municipio = models.PositiveSmallIntegerField()
    nombre = models.CharField(max_length=100)
    djp = models.ForeignKey(DJP, on_delete=models.CASCADE)
    djc = models.ForeignKey(DJC, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Municipios"
        ordering = ['entidad', 'municipio']

    def __str__(self):
        return f"{self.entidad.entidad:02d} - {self.municipio:03d} - {self.nombre.upper()}"

    def get_padron(self):
        return sum(seccion.get_padron() for seccion in self.seccion_set.all() if seccion.get_padron() is not None)

    def get_lista_nominal(self):
        return sum(seccion.get_lista_nominal() for seccion in self.seccion_set.all() if seccion.get_lista_nominal() is not None)

    def get_fecha_corte(self):
        # Assuming you have a related model that stores the date
        latest_estadistico = self.seccion_set.first().estadisticos.latest('historico__fecha')
        return latest_estadistico.historico.fecha if latest_estadistico else None


class ZORE(models.Model):
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)
    distrito = models.ForeignKey(DistritoFederal, on_delete=models.CASCADE)
    zore = models.PositiveSmallIntegerField()
    activa = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.distrito.distrito_federal} - {self.zore:03d}"

    def get_padron(self):
        return sum(are.get_padron() for are in self.are_set.all())

    def get_lista_nominal(self):
        return sum(are.get_lista_nominal() for are in self.are_set.all())

    def get_fecha_corte(self):
        latest_estadistico = EstadisticoSeccion.objects.filter(seccion__are__zore=self).latest('historico__fecha')
        return latest_estadistico.historico.fecha if latest_estadistico else None


class ARE(models.Model):
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)
    zore = models.ForeignKey(ZORE, on_delete=models.CASCADE)
    are = models.PositiveSmallIntegerField()
    activa = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.zore.distrito:02d} - {self.zore.zore:03d} - {self.are:03d}"

    def get_padron(self):
        return sum(seccion.get_padron() for seccion in self.seccion_set.all())

    def get_lista_nominal(self):
        return sum(seccion.get_lista_nominal() for seccion in self.seccion_set.all())

    def get_fecha_corte(self):
        latest_estadistico = EstadisticoSeccion.objects.filter(seccion__are=self).latest('historico__fecha')
        return latest_estadistico.historico.fecha if latest_estadistico else None


class Seccion(models.Model):
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)
    distrito_federal = models.ForeignKey(DistritoFederal, on_delete=models.CASCADE)
    distrito_local = models.ForeignKey(DistritoLocal, on_delete=models.CASCADE)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)
    are = models.ForeignKey(ARE, on_delete=models.CASCADE, null=True, blank=True)
    seccion = models.PositiveSmallIntegerField()
    tipo = models.PositiveSmallIntegerField(choices=TIPO_SECCION)
    activa = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Sección"
        verbose_name_plural = "Secciones"
        ordering = ['entidad', 'municipio', 'seccion']

    def __str__(self):
        return f"{self.entidad.entidad:02d} - {self.municipio.municipio:03d} - {self.seccion:04d}"

    def get_padron(self):
        estadisticos = self.estadisticos.all()
        if estadisticos.exists():
            return estadisticos.latest('historico__fecha').pe
        return None

    def get_lista_nominal(self):
        estadisticos = self.estadisticos.all()
        if estadisticos.exists():
            return estadisticos.latest('historico__fecha').ln
        return None


class HistoricoPE(models.Model):
    fecha = models.DateField(default=timezone.now)
    observaciones = models.TextField(blank=True, null=True)
    pe = models.PositiveIntegerField(blank=True, null=True)
    ln = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        ordering = ['-fecha']  # Ordenar por fecha en orden descendente

    def __str__(self):
        return f"{self.fecha}: PE: {self.pe} - LN: {self.ln}"


class EstadisticoSeccion(models.Model):
    historico = models.ForeignKey(HistoricoPE, on_delete=models.CASCADE, related_name='estadisticos')
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE, related_name='estadisticos')
    pe = models.PositiveIntegerField()
    ln = models.PositiveIntegerField()

    class Meta:
        get_latest_by = 'historico__fecha'

    def __str__(self):
        return f"Entidad: {self.entidad}, Seccion: {self.seccion}, PE: {self.pe}, LN: {self.ln}"
