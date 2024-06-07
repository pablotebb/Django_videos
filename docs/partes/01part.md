## PASOS:

1.  Tenemos instalado Django?

    > py -m django --version

    (Mirar FAQs, si quieres instalar Django desde una virtualización)

    [FAQs](../Faq.md)

2.  Vamos a proyecto_videos/setting.py

    ```python
    from django.contrib import admin
    from django.urls import include, path

    urlpatterns = [
        path('polls/', include('app_videos.urls')),
        path('admin/', admin.site.urls),
    ]
    ```

3.  Vamos a app_videos/urls.py

    ```python
    from django.urls import path
    from . import views

    urlpatterns = [
        path("", views.index, name="index"),
    ]
    ```

4.  Vamos a app_videos/views.py

    ```python
    from django.http import HttpResponse

    def index(request):
      return HttpResponse("Hola mundo. Tu estás en el fichero Encuestas.")
    ```

5.  Miramos app_videos/apps.py

    ```python
    from django.apps import AppConfig


    class AppVideosConfig(AppConfig):
        default_auto_field = 'django.db.models.BigAutoField'
        name = 'app_videos'
    ```

6.  Modificamos proyecto_videos/settings.py:

    ```python
    INSTALLED_APPS = [
        'app_videos.apps.AppVideosConfig',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ]
    ```

7) Ejecutamos:

   > py manage.py runserver

   > http://127.0.0.1:8000/videos/

8) Instalamos Django Allauth (para la gestión de usuarios):

   > pip install django-allauth

9) Modificamos proyecto_videos/urls.py:

   ```python
   from django.contrib import admin
   from django.urls import include, path

   urlpatterns = [
       path('admin/', admin.site.urls),
       path('accounts/', include('allauth.urls')),
       path('', include('app_videos.urls')),
   ]
   ```

10) Configuramos proyecto_videos/settings.py

```python
  AUTHENTICATION_BACKENDS = (
      'django.contrib.auth.backends.ModelBackend',
      'allauth.account.auth_backends.AuthenticationBackend',
  )

  SITE_ID = 1

  ACCOUNT_EMAIL_REQUIRED = True
  ACCOUNT_AUTHENTICATION_METHOD = 'email'
  ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
```

11. Creamos app_videos/models.py

```python
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    youtube_url = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.username
```

12. Creamos una señal para crear el perfil automáticamente, en app_videos/signals.py:

```python
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

```

13. Registramos las señales, en app_videos/apps.py

```python
from django.apps import AppConfig

class AppVideosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_videos'

    def ready(self):
        import app_videos.signals
```

14. Creamos app_videos/forms.py

```python
from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['youtube_url']
```

15. Creamos las vistas y plantillas

> app_views/views.py

```python
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm

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

```

> app_videos/urls.py

```python

from django.urls import path
from . import views

urlpatterns = [
   path('profile/', views.profile_view, name='profile'),
]

```

16. Creamos la plantilla en: app_videos/templates/app_videos/profile.html

```python
<!DOCTYPE html>
<html>
<head>
    <title>Profile</title>
</head>
<body>
    <h1>Profile Page</h1>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Save</button>
    </form>
    {% if request.user.profile.youtube_url %}
        <h2>Your YouTube Video</h2>
        <iframe width="560" height="315" src="https://www.youtube.com/embed/{{ request.user.profile.youtube_url|cut:'https://www.youtube.com/watch?v=' }}" frameborder="0" allowfullscreen></iframe>
    {% endif %}
</body>
</html>
```

17. Migramos y probamos:

> Hacemos migraciones

```python
python manage.py makemigrations
python manage.py migrate
```

> Creamos superusuario (opcional)

> python manage.py createsuperuser

> Ejecutamos el servidor:

> python manage.py runserver
