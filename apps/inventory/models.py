from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


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
	nombre = models.CharField(max_length=30, blank=False)

	def __str__(self):
		return self.nombre

	class Meta:
		verbose_name = "Aplicacion"
		verbose_name_plural = "Aplicaciones"


class Modulo(models.Model):

	aplicacion = models.ForeignKey(Aplicacion, on_delete=models.CASCADE, null=True)	
	nombre = models.CharField(max_length=30, blank=False)

	def __str__(self):
		return self.nombre

	class Meta:
		verbose_name = "Modulo"
		verbose_name_plural = "Modulos"


class TipoFuncionalidad(models.Model):

	nombre = models.CharField(max_length=15, blank=False)

	def __str__(self):
		return self.nombre

	class Meta:
		verbose_name = "Tipo de funcionalidad"
		verbose_name_plural = "Tipos de funcionalidades"


class Funcionalidad(models.Model):

	modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, null=True)	
	codigo = models.CharField(max_length=30, blank=False)
	tipo_funcionalidad = models.ForeignKey(TipoFuncionalidad, on_delete=models.SET_NULL, null=True)
	descripcion = models.CharField(max_length=255, blank=False)
	observacion = models.CharField(max_length=1000, blank=True)

	def __str__(self):
		return self.codigo 

	class Meta:
		verbose_name = "Funcionalidad"
		verbose_name_plural = "Funcionalidades"

