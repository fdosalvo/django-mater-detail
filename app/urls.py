from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mi_app.urls')),  # Incluye las URLs de mi_app
]
