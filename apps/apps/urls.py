from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('compsender/', include('compsender.urls')),
    path('admin/', admin.site.urls),
]
