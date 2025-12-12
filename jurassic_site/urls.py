





from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ajouter/', views.ajouter_dino, name='ajouter_dino'),
    path('liste/', views.liste_dinos, name='liste_dinos'),
    path('enclos/', views.enclos, name='enclos'),
    path('enclos/', views.enclos, name='enclos'),
    path('api/compatibles/<str:dino_ids>/', views.get_compatibles, name='get_compatibles'),
    path('modifier/<int:dino_id>/', views.modifier_dino, name='modifier_dino'),
    path('supprimer/<int:dino_id>/', views.supprimer_dino, name='supprimer_dino'),
    path('', views.home, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)