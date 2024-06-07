"""
URL configuration for proyecto_videos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin # Importa el módulo admin para el sitio de administración
from django.urls import include, path # Importa las funciones include y path para definir rutas URL


urlpatterns = [
    # Incluye las rutas de la aplicación polls bajo el prefijo polls/
    # Esto significa que cualquier URL que comience con app_videos/ será manejada por app_videos.urls
       # path('videos/', include('app_videos.urls')),
    # Define la ruta para el sitio de administración de Django
    # Cuando el usuario accede a /admin/, se mostrará la interfaz de administración
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('app_videos.urls')),
]
