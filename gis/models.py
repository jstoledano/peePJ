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


class Distrito_Federal(models.Model):
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)
    distrito_federal = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = "Distrito"
        verbose_name_plural = "Distritos"
        ordering = ['entidad', 'distrito_federal']

    def __str__(self):
        return f"{self.entidad.entidad:02d} - {self.distrito_federal:02d}"


class Distrito_Local(models.Model):
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
    djp = models.PositiveSmallIntegerField()
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre}"


class DJC(models.Model):
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)
    djc = models.PositiveSmallIntegerField()
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre}"


class Municipio(models.Model):
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)
    municipio = models.PositiveSmallIntegerField()
    nombre = models.CharField(max_length=100)
    djp = models.ForeignKey(DJP, on_delete=models.CASCADE)
    djc = models.ForeignKey(DJC, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.entidad.entidad:02d} - {self.municipio:03d} - {self.nombre.upper()}"


class ZORE(models.Model):
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)
    zore = models.PositiveSmallIntegerField()
    activa = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.seccion.distrito_federal:02d} - {self.zore:03d}"


class ARE(models.Model):
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)
    are = models.PositiveSmallIntegerField()
    zore = models.ForeignKey(ZORE, on_delete=models.CASCADE)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.seccion.distrito_federal:02d} - {self.zore:03d} - {self.are:03d}"


class Seccion(models.Model):
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)
    distrito_federal = models.ForeignKey(Distrito_Federal, on_delete=models.CASCADE)
    distrito_local = models.ForeignKey(Distrito_Local, on_delete=models.CASCADE)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)
    are = models.ForeignKey(ARE, on_delete=models.CASCADE)
    seccion = models.PositiveSmallIntegerField()
    tipo = models.PositiveSmallIntegerField(choices=TIPO_SECCION)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.entidad.entidad:02d} - {self.municipio:03d} - {self.seccion:04d}"
