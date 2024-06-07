from django.http import HttpResponse # Importa la clase HttpResponse para enviar respuestas HTTP simples
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm

def index(request):
  # Define la vista index que maneja las solicitudes a una URL específica
  # request: El objeto HttpRequest que contiene datos sobre la solicitud
  return HttpResponse("Hola mundo. Tu estás en el fichero Encuestas.")
  # Retorna una respuesta HTTP con el texto "Hola mundo. Tú estás en el fichero Encuestas."
  
@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'core/profile.html', {'form': form})
