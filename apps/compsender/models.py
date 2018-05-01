from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class TipoComprobante(models.Model):

	codigo = models.CharField(max_length=2, blank=False)
	name = models.CharField(max_length=30, blank=False)

	def __str__(self):
		return self.name


class Comprobante(models.Model):

	document = models.FileField(upload_to='documents/')
	uploaded_at = models.DateTimeField(auto_now_add=True)
	cuit_emisor = models.CharField(max_length=11, blank=True)
	tipo_comprobante = models.ForeignKey(TipoComprobante, on_delete=models.SET_NULL, null=True)
	punto_venta = models.IntegerField(blank=True)
	numero_comprobante = models.IntegerField(blank=True)
	fecha_emision = models.DateField(auto_now_add=True,blank=True)
	cae = models.CharField(max_length=14, blank=True)
	cae_vto = models.DateField(auto_now_add=True,blank=True)
	importe_total = models.DecimalField(max_digits=15, decimal_places=2,blank=True)
	importe_gravado = models.DecimalField(max_digits=15, decimal_places=2,blank=True)
	importe_no_gravado = models.DecimalField(max_digits=15, decimal_places=2,blank=True)
	importe_otros_impuestos = models.DecimalField(max_digits=15, decimal_places=2,blank=True)
	iva_21 = models.DecimalField(max_digits=15, decimal_places=2,blank=True)
	iva_10_5 = models.DecimalField(max_digits=15, decimal_places=2,blank=True)
	iva_27 = models.DecimalField(max_digits=15, decimal_places=2,blank=True)
	iva_5 = models.DecimalField(max_digits=15, decimal_places=2,blank=True)
	iva_2_5 = models.DecimalField(max_digits=15, decimal_places=2,blank=True)

	def clean(self):

		errors = []

		########################################################################################
		# Punto de venta
		########################################################################################
		if not self.punto_venta:
			errors.append(_('El punto de venta es obligatorio'))
		if self.punto_venta <1 or self.punto_venta > 9999:
			errors.append(_('El punto de venta debe debe ser un valor entre 1 y 9999'))

		########################################################################################
		# número de comprobante
		########################################################################################
		if not self.numero_comprobante:
			errors.append(_('El punto de venta es obligatorio'))
		if self.numero_comprobante < 1 or self.numero_comprobante > 9999:
			errors.append(_('El número de comprobante debe debe ser un valor entre 1 y 99.999.999'))

		if errors:
			raise ValidationError(errors)


