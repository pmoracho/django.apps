from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('compsender/', include('compsender.urls')),
    path('inventory', include('inventory.urls')),
    path('admin/', admin.site.urls),
	# path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
]

from django.conf import settings
from django.conf.urls import include, url

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
