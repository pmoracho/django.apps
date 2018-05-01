from django.contrib import admin

from .models import TipoComprobante
from .models import Comprobante

admin.site.register(TipoComprobante)
admin.site.register(Comprobante)
