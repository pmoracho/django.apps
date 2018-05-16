from django.contrib import admin

from .models import Area
from .models import Proyecto
from .models import Sistema
from .models import Aplicacion
from .models import Modulo
from .models import TipoFuncionalidad
from .models import Funcionalidad

admin.site.site_header = "Apps Inventory ";
admin.site.site_title = "Apps Inventory ";

admin.site.register(Area)
admin.site.register(Proyecto)
admin.site.register(Sistema)
admin.site.register(Aplicacion)
admin.site.register(Modulo)
admin.site.register(TipoFuncionalidad)

class FuncionalidadAdmin(admin.ModelAdmin):
	search_fields = ['modulo', 'codigo', 'tipo_funcionalidad', 'descripcion', 'observacion']
	list_display = ('proyecto', 'area', 'sistema', 'aplicacion', 'modulo','codigo','tipo_funcionalidad', 'descripcion')
	list_filter = ('modulo','codigo','tipo_funcionalidad', 'descripcion')

	def aplicacion(self, obj):
		return obj.modulo.aplicacion

	def sistema(self, obj):
		return obj.modulo.aplicacion.sistema

	def area(self, obj):
		return obj.modulo.aplicacion.sistema.area

	def proyecto(self, obj):
		return obj.modulo.aplicacion.sistema.area.proyecto

admin.site.register(Funcionalidad, FuncionalidadAdmin)
