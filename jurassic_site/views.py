from django.shortcuts import render, redirect, get_object_or_404
from .forms import DinosaureAddForm, DinosaureEditForm
from .models import Dinosaure
from django.http import HttpResponseRedirect
from django.urls import reverse

# Page d'accueil (liste des dinos)
def home(request):
    return render(request, 'home.html')

def liste(request):
    dinos = Dinosaure.objects.all()
    return render(request, 'dinos_list.html', {'dinos': dinos})
# Ajouter un dinosaure
def ajouter_dino(request):
    if request.method == 'POST':
        form = DinosaureAddForm(request.POST, request.FILES)
        if form.is_valid():
            dino = form.save(commit=False)  # On crée le dino sans sauvegarder encore les M2M
            dino.save()  # On sauvegarde l'objet principal
            form.save_m2m()  # Maintenant on peut sauvegarder les champs ManyToMany
            return redirect('home')
    else:
        form = DinosaureAddForm()
    return render(request, 'ajouter_dino.html', {'form': form})

# Modifier un dinosaure pour ajouter "aime" et "n'aime pas"
def modifier_dino(request, dino_id):
    dino = get_object_or_404(Dinosaure, id=dino_id)
    if request.method == 'POST':
        form = DinosaureEditForm(request.POST, request.FILES, instance=dino)
        if form.is_valid():
            if 'image' in request.FILES and dino.image:
                dino.image.delete(save=False)
            form.save()
            return redirect('home')
    else:
        form = DinosaureEditForm(instance=dino)
    return render(request, 'formulaire_dino.html', {'form': form, 'dino': dino})


def liste_dinos(request):
    print("View liste_dinos appelée")

    type_filtre = request.GET.get('type', '')  # Récupère le filtre depuis l'URL

    # Si un type est choisi, on filtre
    if type_filtre and type_filtre != 'Tous':
        dinos = Dinosaure.objects.filter(type=type_filtre)

    else:
        dinos = Dinosaure.objects.all()


    # On récupère la liste des types possibles
    types_disponibles = [choice[0] for choice in Dinosaure.TYPE_CHOICES]
    types_disponibles.insert(0, "Tous")

    return render(request, 'dinos_list.html', {
        'dinos': dinos,
        'type_filtre': type_filtre,
        'types_disponibles': types_disponibles
    })
def supprimer_dino(request, dino_id):
    dino = get_object_or_404(Dinosaure, id=dino_id)
    if request.method == "POST":
        dino.delete()
        return redirect('liste_dinos')
    return render(request, 'supprimer_dino.html', {'dino': dino})

def enclos(request):
    return render(request, 'enclos.html')