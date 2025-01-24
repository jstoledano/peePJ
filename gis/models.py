from django.utils import timezone
from django.db import models
from django.db.models import Sum


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


class DistritoFederal(models.Model):
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)
    distrito_federal = models.PositiveSmallIntegerField("Distrito")

    class Meta:
        verbose_name = "Distrito"
        verbose_name_plural = "Distritos"
        ordering = ['entidad', 'distrito_federal']

    def __str__(self):
        return f"{self.entidad.entidad:02d} - {self.distrito_federal:02d}"

    def get_pe(self):
        return self.seccion_set.aggregate(suma_padron=Sum('padron__pe'))['suma_padron']

    def get_ln(self):
        return self.seccion_set.aggregate(suma_lista_nominal=Sum('padron__ln'))['suma_lista_nominal']


class DistritoLocal(models.Model):
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)
    distrito_local = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = "Distrito Local"
        verbose_name_plural = "Distritos Locales"
        ordering = ['entidad', 'distrito_local']

    def __str__(self):
        return f"{self.entidad.entidad:02d} - {self.distrito_local:02d}"

    def get_pe(self):
        return self.seccion_set.aggregate(suma_padron=Sum('padron__pe'))['suma_padron']

    def get_ln(self):
        return self.seccion_set.aggregate(suma_lista_nominal=Sum('padron__ln'))['suma_lista_nominal']


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

    def get_pe(self):
        return self.seccion_set.aggregate(suma_padron=Sum('padron__pe'))['suma_padron']

    def get_ln(self):
        return self.seccion_set.aggregate(suma_lista_nominal=Sum('padron__ln'))['suma_lista_nominal']


class ZORE(models.Model):
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)
    distrito = models.ForeignKey(DistritoFederal, on_delete=models.CASCADE)
    zore = models.PositiveSmallIntegerField()
    activa = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.distrito.distrito_federal} - {self.zore:03d}"


class ARE(models.Model):
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)
    zore = models.ForeignKey(ZORE, on_delete=models.CASCADE)
    are = models.PositiveSmallIntegerField()
    activa = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.zore.distrito:02d} - {self.zore.zore:03d} - {self.are:03d}"

    def get_pe(self):
        return self.seccion_set.aggregate(suma_padron=Sum('padron__pe'))['suma_padron']

    def get_ln(self):
        return self.seccion_set.aggregate(suma_lista_nominal=Sum('padron__ln'))['suma_lista_nominal']


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


class Padron(models.Model):
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE)
    pe = models.PositiveIntegerField("PE")
    ln = models.PositiveIntegerField("LN")

    class Meta:
        verbose_name = "PE y LN"
        verbose_name_plural = "PE y LN"
        ordering = ['entidad', 'seccion']

    def __str__(self):
        return f"{self.entidad.entidad} {self.seccion.seccion:04d} - Padron: {self.pe} - Lista Nominal: {self.ln}"
