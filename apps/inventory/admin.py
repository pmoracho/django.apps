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
from .models import TipoEntidad
from .models import Entidad

from import_export.admin import ImportExportActionModelAdmin
from import_export import resources

admin.site.site_header = "Apps Inventory ";
admin.site.site_title = "Apps Inventory ";

admin.site.register(Proyecto)
admin.site.register(Sistema)
admin.site.register(Aplicacion)
admin.site.register(Modulo)
admin.site.register(TipoFuncionalidad)
admin.site.register(TipoEntidad)

class AreaAdmin(ImportExportActionModelAdmin):
	pass

class FuncionalidadEntidadInline(admin.TabularInline):
	model = Funcionalidad.entidades.through
	suit_classes = 'suit-tab suit-tab-entidades'
	extra = 1

class FuncionalidadResource(resources.ModelResource):

	class Meta:
		model = Funcionalidad
		fields = (	'modulo__aplicacion__sistema__area__nombre',
					'modulo__aplicacion__sistema__nombre',
					'modulo__aplicacion__nombre',
					'modulo__nombre',
					'codigo',
					'descripcion',
					'tipo__nombre',
					'observacion',
					'entrada_usuario',
					'salida_usuario',
					'funcionalidadentidad__entidad__id'
				)

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
	list_display = ('origen', 'tipo', 'nombre',)
	list_filter = ('origen', 'tipo', 'nombre',)

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


# class FuncionalidadAdmin(admin.ModelAdmin):
class FuncionalidadAdmin(ImportExportActionModelAdmin):

	form = FuncionalidadModelForm
	search_fields = ['modulo', 'entidad', 'codigo', 'tipo', 'descripcion', 'observacion', 'aplicacion']
	list_display = ('modulo', 'codigo', 'descripcion', 'grupo', 'proyecto', 'area', 'sistema', 'aplicacion', 'tipo')
	list_filter = ('modulo__aplicacion__sistema__area', 'modulo__aplicacion__sistema','modulo__aplicacion', 'modulo','codigo','tipo', 'descripcion', EntidadFilter, )

	inlines = (FuncionalidadEntidadInline, )
	actions = [duplicate_event]
	resource_class = FuncionalidadResource
	save_as = True

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

	def grupo(self, obj):
		return obj.modulo.grupo

	def aplicacion(self, obj):
		return obj.modulo.aplicacion

	def sistema(self, obj):
		return obj.modulo.aplicacion.sistema

	def area(self, obj):
		return obj.modulo.aplicacion.sistema.area

	def proyecto(self, obj):
		return obj.modulo.aplicacion.sistema.area.proyecto

	# def save_model(self, request, obj, form, change):
	# 	# Django always sends this when "Save as new is clicked"
	# 	if '_saveasnew' in request.POST:
	# 		# Get the ID from the admin URL
	# 		original_pk = resolve(request.path).args[0]
	# 		# Get the original object
	# 		original_obj = obj._meta.concrete_model.objects.get(id=original_pk)

	# 		# Iterate through all it's properties
	# 		for prop, value in vars(original_obj).iteritems():
	# 			# if the property is an Image (don't forget to import ImageFieldFile!)
	# 			if isinstance(getattr(original_obj, prop), FieldFile):
	# 				setattr(obj,prop,getattr(original_obj, prop)) # Copy it!
	# 	obj.save()


admin.site.register(Funcionalidad, FuncionalidadAdmin)
admin.site.register(Entidad, EntidadAdmin)
admin.site.register(Area, AreaAdmin)
