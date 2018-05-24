from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class Proyecto(models.Model):

	nombre = models.CharField(max_length=30, blank=False)

	def __str__(self):
		return self.nombre

	class Meta:
		verbose_name = "Proyecto"
		verbose_name_plural = "Proyectos"

class Area(models.Model):

	proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, null=True)
	nombre = models.CharField(max_length=30, blank=False)

	def __str__(self):
		return self.nombre

	class Meta:
		verbose_name = "Area"
		verbose_name_plural = "Areas"


class Sistema(models.Model):

	area = models.ForeignKey(Area, on_delete=models.CASCADE, null=True)
	nombre = models.CharField(max_length=30, blank=False)

	def __str__(self):
		return self.nombre

	class Meta:
		verbose_name = "Sistemas"
		verbose_name_plural = "Sistemas"


class Aplicacion(models.Model):

	sistema = models.ForeignKey(Sistema, on_delete=models.CASCADE, null=True)
	nombre = models.CharField(max_length=255, blank=False)
	atajo = models.CharField(max_length=255, blank=True)
	grupo = models.CharField(max_length=255, blank=True)
	descripcion = models.CharField(max_length=255, blank=True)

	def __str__(self):
		return self.nombre

	class Meta:
		verbose_name = "Aplicacion"
		verbose_name_plural = "Aplicaciones"


class Modulo(models.Model):

	aplicacion = models.ForeignKey(Aplicacion, on_delete=models.CASCADE, null=True)
	codigo = models.CharField(max_length=30, blank=False)
	descripcion = models.CharField(max_length=255, blank=True)

	def __str__(self):
		return self.codigo

	class Meta:
		verbose_name = "Modulo"
		verbose_name_plural = "Modulos"

class TipoFuncionalidad(models.Model):

	nombre = models.CharField(max_length=255, blank=False)
	nombre_corto = models.CharField(max_length=15, blank=False)

	def __str__(self):
		return self.nombre

	class Meta:
		verbose_name = "Tipo de funcionalidad"
		verbose_name_plural = "Tipos de funcionalidades"

class TipoEntidad(models.Model):

	nombre = models.CharField(max_length=15, blank=False)

	def __str__(self):
		return self.nombre

	class Meta:
		verbose_name = "Tipo de entidad"
		verbose_name_plural = "Tipo de entidades"

class Entidad(models.Model):

	origen = models.ForeignKey(Sistema, on_delete=models.CASCADE, null=True)
	tipo = models.ForeignKey(TipoEntidad, on_delete=models.SET_NULL, null=True)
	nombre = models.CharField(max_length=255, blank=False)
	descripcion = models.CharField(max_length=255, blank=True)

	def __str__(self):
		return "{0}.{1}".format(self.origen,self.nombre)

	class Meta:
		verbose_name = "Entidad"
		verbose_name_plural = "Entidades"


class Funcionalidad(models.Model):

	modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, null=True)
	codigo = models.CharField(max_length=30, blank=False)
	tipo = models.ForeignKey(TipoFuncionalidad, on_delete=models.SET_NULL, null=True)
	descripcion = models.CharField(max_length=255, blank=False)
	observacion = models.CharField(max_length=1000, blank=True)
	entrada_usuario = models.CharField(max_length=255, blank=True)
	salida_usuario = models.CharField(max_length=255, blank=True)
	entidades = models.ManyToManyField(Entidad, through='FuncionalidadEntidad')

	def __str__(self):
		return self.codigo

	def get_all(self):
		return

	class Meta:
		verbose_name = "Funcionalidad"
		verbose_name_plural = "Funcionalidades"


class FuncionalidadEntidad(models.Model):

	entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE, null=True)
	funcionalidad = models.ForeignKey(Funcionalidad, on_delete=models.CASCADE, null=True)
	modo = models.ForeignKey(TipoFuncionalidad, on_delete=models.SET_NULL, null=True)
	observacion = models.CharField(max_length=1000, blank=True)

	def __str__(self):
		return "{0}.{1}.{2}".format(self.funcionalidad,self.entidad, self.modo)

	class Meta:
		verbose_name = "Entidad por funcionalidad"
		verbose_name_plural = "Entidades por funcionalidad"


class UserGroup(models.Model):
    class Meta:
        permissions = (
            ('can_view_lizard_data', _('Can add user')),
            #                       ^^^ note the _() translation marker.
            )
