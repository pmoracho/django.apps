from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('compsender/', include('compsender.urls')),
    path('inventory', include('inventory.urls')),
    path('admin/', admin.site.urls),
]
