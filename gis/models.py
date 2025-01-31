from django.db import models
from django.db.models import Sum


TIPO_SECCION = (
    (2, 'URBANA'),
    (3, 'MIXTA'),
    (4, 'RURAL')
)


class BaseSeccion(models.Model):
    class Meta:
        abstract = True

    def get_pe(self):
        return self.seccion_set.aggregate(suma_pe=Sum('pe'))['suma_pe']

    def get_ln(self):
        return self.seccion_set.aggregate(suma_ln=Sum('ln'))['suma_ln']


class Entidad(BaseSeccion):
    entidad = models.PositiveSmallIntegerField()
    nombre = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Entidades"
        ordering = ['entidad']

    def __str__(self):
        return f"{self.entidad:02d} - {self.nombre.upper()}"


class DistritoFederal(BaseSeccion):
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)
    distrito_federal = models.PositiveSmallIntegerField("Distrito")

    class Meta:
        verbose_name = "Distrito"
        verbose_name_plural = "Distritos"
        ordering = ['entidad', 'distrito_federal']

    def __str__(self):
        return f"{self.entidad.entidad:02d} - {self.distrito_federal:02d}"


class DistritoLocal(BaseSeccion):
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)
    distrito_local = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = "Distrito Local"
        verbose_name_plural = "Distritos Locales"
        ordering = ['entidad', 'distrito_local']

    def __str__(self):
        return f"{self.entidad.entidad:02d} - {self.distrito_local:02d}"


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

    def get_secciones(self):
        return Seccion.objects.filter(municipio__djp=self).count()

    def get_pe(self):
        return Seccion.objects.filter(municipio__djp=self).aggregate(suma_pe=Sum('pe'))['suma_pe']

    def get_ln(self):
        return Seccion.objects.filter(municipio__djp=self).aggregate(suma_ln=Sum('ln'))['suma_ln']


class CargosDJP(models.Model):
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)
    djp = models.ForeignKey(DJP, on_delete=models.CASCADE)
    cargo = models.CharField(max_length=150)
    puestos = models.PositiveSmallIntegerField

    class Meta:
        verbose_name = "Cargo DJP"
        verbose_name_plural = "Cargos DJP"
        ordering = ['entidad', 'djp', 'cargo']

    def __str__(self):
        return f"{self.entidad.entidad} DJP: {self.djp.nombre} {self.cargo}"


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

    def get_secciones(self):
        return Seccion.objects.filter(municipio__djc=self).count()

    def get_pe(self):
        return Seccion.objects.filter(municipio__djc=self).aggregate(suma_pe=Sum('pe'))['suma_pe']

    def get_ln(self):
        return Seccion.objects.filter(municipio__djc=self).aggregate(suma_ln=Sum('ln'))['suma_ln']


class CargosDJC(models.Model):
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)
    djc = models.ForeignKey(DJC, on_delete=models.CASCADE)
    cargo = models.CharField(max_length=150)
    puestos = models.PositiveSmallIntegerField

    class Meta:
        verbose_name = "Cargo DJC"
        verbose_name_plural = "Cargos DJC"
        ordering = ['entidad', 'djc', 'cargo']

    def __str__(self):
        return f"{self.entidad.entidad} DJC: {self.djc.nombre} {self.cargo}"


class Municipio(BaseSeccion):
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


class ZORE(models.Model):
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)
    distrito = models.ForeignKey(DistritoFederal, on_delete=models.CASCADE)
    zore = models.PositiveSmallIntegerField()
    activa = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.distrito.distrito_federal} - {self.zore:03d}"


class ARE(BaseSeccion):
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)
    zore = models.ForeignKey(ZORE, on_delete=models.CASCADE)
    are = models.PositiveSmallIntegerField()
    activa = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.zore.distrito:02d} - {self.zore.zore:03d} - {self.are:03d}"


class Seccion(models.Model):
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)
    distrito_federal = models.ForeignKey(DistritoFederal, on_delete=models.CASCADE)
    distrito_local = models.ForeignKey(DistritoLocal, on_delete=models.CASCADE)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)
    are = models.ForeignKey(ARE, on_delete=models.CASCADE, null=True, blank=True)
    seccion = models.PositiveSmallIntegerField()
    tipo = models.PositiveSmallIntegerField(choices=TIPO_SECCION)
    pe = models.PositiveIntegerField("PE", null=True, blank=True)
    ln = models.PositiveIntegerField("LN", null=True, blank=True)
    activa = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Sección"
        verbose_name_plural = "Secciones"
        ordering = ['entidad', 'municipio', 'seccion']

    def __str__(self):
        return f"{self.entidad.entidad:02d} - {self.municipio.municipio:03d} - {self.seccion:04d}"


AMBITO = [
    (1, 'NACIONAL'),
    (2, 'CIRCUNSCRIPCION'),
    (3, 'DISTRITO JUDICIAL'),
    (4, 'ESTATAL'),
    (5, 'JUDICIAL PENAL'),
    (6, 'JUDICIAL CIVIL'),
]


