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
		# Documento
		########################################################################################
		if not self.document:
			errors.append(_('El documento es obligatorio'))

		########################################################################################
		# Tipo de comprobante
		########################################################################################
		if self.tipo_comprobante is None:
			errors.append(_('El tipo de comprobante es obligatorio'))

		########################################################################################
		# Punto de venta
		########################################################################################
		if self.punto_venta is None:
			errors.append(_('El punto de venta es obligatorio'))
		elif self.punto_venta <1 or self.punto_venta > 9999:
			errors.append(_('El punto de venta debe debe ser un valor entre 1 y 9999'))

		########################################################################################
		# número de comprobante
		########################################################################################
		if self.numero_comprobante is None:
			errors.append(_('El número de comprobante es obligatorio'))
		elif self.numero_comprobante < 1 or self.numero_comprobante > 9999:
			errors.append(_('El número de comprobante debe debe ser un valor entre 1 y 99.999.999'))

		########################################################################################
		# Cuit del emisor
		########################################################################################
		if self.cuit_emisor is None:
			errors.append(_('El número de CUIT del emisor es obligatorio'))
		elif not validar_cuit(self.cuit_emisor):
			errors.append(_('El número de CUIT es inválido'))

		if errors:
			raise ValidationError(errors)

def validar_cuit(cuit):

	if	len(cuit) != 11 and (len(cuit) != 11 or cuit[2] != "-" or cuit[11] != "-"):
		return False

	base = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]

	cuit = cuit.replace("-", "") # remuevo las barras

	# calculo el digito verificador:
	aux = 0
	for i in range(10):
		aux += int(cuit[i]) * base[i]

	aux = 11 - (aux - (int(aux / 11) * 11))

	if aux == 11:
		aux = 0
	if aux == 10:
		aux = 9

	return aux == int(cuit[10])
