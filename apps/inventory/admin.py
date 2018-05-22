from django.contrib import admin
from django.forms import TextInput, Textarea, ChoiceField
from django.db import models
from django import forms
from django.contrib.admin import SimpleListFilter

from .models import Area
from .models import Proyecto
from .models import Sistema
from .models import Aplicacion
from .models import Modulo
from .models import TipoFuncionalidad
from .models import Funcionalidad
from .models import FuncionalidadEntidad
from .models import TipoEntidad
from .models import Entidad

import io
from django.http.response import HttpResponse
from xlsxwriter.workbook import Workbook


admin.site.site_header = "Apps Inventory ";
admin.site.site_title = "Apps Inventory ";

admin.site.register(Proyecto)
admin.site.register(Sistema)
admin.site.register(TipoFuncionalidad)
admin.site.register(TipoEntidad)


################################################################################
# FORM: Aplicaciones
################################################################################
class AplicacionAdmin(admin.ModelAdmin):
	list_display  = ('sistema_nombre', 'grupo', 'descripcion',)
	search_fields = ('sistema__nombre', 'nombre', 'grupo', 'descripcion',)
	list_filter   = ('sistema', 'nombre', 'grupo',)
	save_as       = True

	def sistema_nombre(self, obj):
		return "{0} - {1}".format(obj.sistema.nombre, obj.nombre)

	sistema_nombre.allow_tags = True
	sistema_nombre.short_description = 'Sistema / Módulo'
	sistema_nombre.admin_order_field = 'sistema'

admin.site.register(Aplicacion, AplicacionAdmin)

################################################################################
# FORM: Area
################################################################################
class AreaAdmin(admin.ModelAdmin):
	list_display  = ('proyecto', 'nombre', 'id')


admin.site.register(Area, AreaAdmin)


class FuncionalidadEntidadInline(admin.TabularInline):
	model = Funcionalidad.entidades.through
	suit_classes = 'suit-tab suit-tab-entidades'
	extra = 1

def duplicate_event(modeladmin, request, queryset):
	for object in queryset:
		object.id = None
		object.save()

duplicate_event.short_description = "Duplicar el/los registros seleccionados"

class FuncionalidadModelForm( forms.ModelForm ):

	descripcion = forms.CharField( widget=forms.Textarea )
	observacion = forms.CharField( widget=forms.Textarea )
	class Meta:
		widgets = {
			'descripcion': Textarea(attrs={'cols': 180, 'rows': 20}),
			'observacion': Textarea(attrs={'cols': 180, 'rows': 20}),
		}

class FuncionalidadGeneral(admin.TabularInline):
	model = Funcionalidad
	suit_classes = 'suit-tab suit-tab-general'

class EntidadAdmin(admin.ModelAdmin):

	search_fields = ['origen', 'tipo', 'nombre']
	list_display = ('origen_nombre', 'tipo', 'id',)
	list_filter = ('origen', 'tipo', 'nombre',)
	save_as       = True

	def origen_nombre(self, obj):
		return "{0} - {1}".format(obj.origen.nombre, obj.nombre)

	origen_nombre.allow_tags = True
	origen_nombre.short_description = 'Origen / Nombre'
	origen_nombre.admin_order_field = 'origen'

class EntidadFilter(SimpleListFilter):

	title = 'Entidad'
	parameter_name = 'entidad'

	def lookups(self, request, model_admin):

		return [(e.id, e.nombre) for e in Entidad.objects.all()]

	def queryset(self, request, queryset):

		if self.value():
			return Funcionalidad.objects.filter(funcionalidadentidad__entidad__id = self.value())
		else:
			return queryset

def funcionalidades_generate_xlsx(modeladmin, request, queryset):

	output = io.BytesIO()

	workbook = Workbook(output, {'in_memory': True})
	worksheet = workbook.add_worksheet()

	titulos = [	('Area', 10.5), 
				('Sistema', 6),
				('Opción de menu (completa con /)', 38),
				('Aplicación', 15),
				('Módulo', 15),
				('Funcionalidad', 15),
				('Descripción', 36),
				('E usuario', 18),
				('S usuario', 18),
				('Modo', 5),
				('Entidad/Información', 32),
				('Observaciones', 42)]

	fmtheader = workbook.add_format({
		'bold': True,
		'font_size': 8,
		'font': 'Calibri', 
		'bg_color': '#F7F7F7',
		'color': 'black',
		'align': 'center',
		'valign': 'top',
		'border': 1
	})
	fmtcell = workbook.add_format({
		'bold': False,
		'font_size': 8,
		'font': 'Calibri', 
		'valign': 'top',
		'border': 1,
		'text_wrap': True
	})

	row = 0
	for i,t in enumerate(titulos):
		worksheet.write(row, i, t[0], fmtheader)
		worksheet.set_column(i, i, t[1])
	row = 1
	for funcionalidad in queryset:

		worksheet.write(row, 0, funcionalidad.modulo.aplicacion.sistema.area.nombre, fmtcell)
		worksheet.write(row, 1, funcionalidad.modulo.aplicacion.sistema.nombre, fmtcell)
		worksheet.write(row, 2, funcionalidad.modulo.aplicacion.atajo, fmtcell)
		worksheet.write(row, 3, funcionalidad.modulo.aplicacion.nombre, fmtcell)
		worksheet.write(row, 4, funcionalidad.modulo.nombre, fmtcell)
		worksheet.write(row, 5, funcionalidad.codigo, fmtcell)
		worksheet.write(row, 6, funcionalidad.descripcion, fmtcell)
		worksheet.write(row, 7, funcionalidad.entrada_usuario, fmtcell)
		worksheet.write(row, 8, funcionalidad.salida_usuario, fmtcell)
		worksheet.write(row, 9, funcionalidad.tipo.nombre_corto, fmtcell)
		worksheet.write(row,11, funcionalidad.observacion, fmtcell)

		entidades = funcionalidad.entidades.all()
		if entidades:
			for entidad in entidades:
				fe = FuncionalidadEntidad.objects.get(funcionalidad=funcionalidad, entidad=entidad)
				worksheet.write(row,10, "{0}: {1}".format(fe.modo.nombre_corto,entidad.nombre), fmtcell)
				row = row + 1
		else:
			row = row + 1

	workbook.close()

	output.seek(0)
	response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
	response['Content-Disposition'] = "attachment; filename=funcionalidades.xlsx"
	output.close()

	return response

funcionalidades_generate_xlsx.short_description = u"Generar planilla de funcionalidades"

################################################################################
# FORM: Modulo
################################################################################
class ModuloAdmin(admin.ModelAdmin):
	list_display  = ('aplicacion_modulo', 'descripcion', 'id')
	list_filter   = ('aplicacion__nombre', 'nombre',)
	search_fields = ('aplicacion__nombre', 'nombre')
	save_as       = True

	def aplicacion_modulo(self, obj):
		return "{0} - {1}".format(obj.aplicacion.nombre, obj.nombre)

admin.site.register(Modulo, ModuloAdmin)



	# def sistema_nombre(self, obj):
	# 	return "{0} - {1}".format(obj.sistema.nombre, obj.nombre)

	# sistema_nombre.allow_tags = True
	# sistema_nombre.short_description = 'Sistema / Módulo'
	# sistema_nombre.admin_order_field = 'sistema'

################################################################################
# FORM: Modulo
################################################################################
class FuncionalidadAdmin(admin.ModelAdmin):

	form          = FuncionalidadModelForm
	search_fields = ['modulo', 'entidad', 'codigo', 'tipo', 'descripcion', 'observacion', 'aplicacion']
	list_filter   = ('modulo__aplicacion__sistema__area', 'modulo__aplicacion__sistema','modulo__aplicacion', 'modulo','codigo','tipo', 'descripcion', EntidadFilter, )
	list_display  = ('modulo_codigo', 'descripcion', 'grupo', 'proyecto', 'area', 'sistema', 'aplicacion', 'tipo', 'id')

	inlines       = (FuncionalidadEntidadInline, )
	actions       = [duplicate_event, funcionalidades_generate_xlsx]
	save_as       = True

	fieldsets = [
		(None, {
	 			'classes': ('suit-tab', 'suit-tab-general', ),
				'fields': ['modulo', 'codigo', 'tipo', 'descripcion', 'observacion','entrada_usuario', 'salida_usuario']
				}
		),
	]
	suit_form_tabs = (
					('general', 'General'),
					('entidades', 'Entidades')
	)

	def modulo_codigo(self, obj):
		return "{0} - {1}".format(obj.modulo.nombre, obj.codigo)

	modulo_codigo.allow_tags = True
	modulo_codigo.short_description = 'Módulo/Código'
	modulo_codigo.admin_order_field = 'modulo'

	def grupo(self, obj):
		return obj.modulo.aplicacion.grupo

	def aplicacion(self, obj):
		return obj.modulo.aplicacion

	def sistema(self, obj):
		return obj.modulo.aplicacion.sistema

	def area(self, obj):
		return obj.modulo.aplicacion.sistema.area

	def proyecto(self, obj):
		return obj.modulo.aplicacion.sistema.area.proyecto


admin.site.register(Funcionalidad, FuncionalidadAdmin)
admin.site.register(Entidad, EntidadAdmin)
