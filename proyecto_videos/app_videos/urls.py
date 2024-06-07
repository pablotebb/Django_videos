from django.urls import path  # Importa la función path para definir rutas URL
from . import views # Importa el módulo views desde el paquete actual

urlpatterns = [
   # Define una ruta URL para la raíz de la aplicación polls
   # Llama a la vista index cuando el usuario accede a /polls/
   path("", views.index, name="index"),
   path('profile/', views.profile_view, name='profile'),
]
