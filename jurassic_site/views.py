from django.shortcuts import render, redirect, get_object_or_404
from .forms import DinosaureAddForm, DinosaureEditForm
from .models import Dinosaure
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse


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
    dinos = Dinosaure.objects.all()
    return render(request, 'enclos.html', {'dinos': dinos})





def enclos(request):
    """Page principale de l'enclos"""
    dinosaures = Dinosaure.objects.all().order_by('nom')
    return render(request, 'enclos.html', {'dinosaures': dinosaures})


def verifier_compatibilite(dino1, dino2):
    """
    Vérifie si deux dinosaures sont compatibles
    Retourne (compatible: bool, raison: str)
    """

    # Règles de base par type (environnement)
    types_aquatiques = ['Reptile marin']
    types_aeriens = ['Reptile volant']
    types_terrestres = ['Carnivore', 'Herbivore', 'Piscivore']

    # 1. Les reptiles marins sont uniquement compatibles entre eux
    if dino1.type in types_aquatiques or dino2.type in types_aquatiques:
        if dino1.type == dino2.type == 'Reptile marin':
            # Vérifier les autres règles pour les reptiles marins entre eux
            pass
        else:
            return False, "Les reptiles marins nécessitent un enclos aquatique séparé"

    # 2. Les reptiles volants sont uniquement compatibles entre eux
    if dino1.type in types_aeriens or dino2.type in types_aeriens:
        if dino1.type == dino2.type == 'Reptile volant':
            # Vérifier les autres règles pour les reptiles volants entre eux
            pass
        else:
            return False, "Les reptiles volants nécessitent une volière séparée"

    # 3. Les carnivores ne sont pas compatibles avec les herbivores
    if (dino1.type == 'Carnivore' and dino2.type == 'Herbivore') or \
            (dino1.type == 'Herbivore' and dino2.type == 'Carnivore'):
        return False, "Les carnivores et herbivores ne peuvent pas cohabiter"

    # 4. Les piscivores ne sont compatibles ni avec carnivores ni avec herbivores
    if dino1.type == 'Piscivore' and dino2.type in ['Carnivore', 'Herbivore']:
        return False, "Les piscivores ne sont pas compatibles avec ce type"
    if dino2.type == 'Piscivore' and dino1.type in ['Carnivore', 'Herbivore']:
        return False, "Les piscivores ne sont pas compatibles avec ce type"

    # 5. Vérifier les incompatibilités individuelles
    if dino2 in dino1.naime_pas.all():
        return False, f"{dino1.nom} n'aime pas {dino2.nom}"
    if dino1 in dino2.naime_pas.all():
        return False, f"{dino2.nom} n'aime pas {dino1.nom}"

    # 6. Vérifier les incompatibilités de type
    if dino1.naime_pas_types:
        types_interdits = [t.strip() for t in dino1.naime_pas_types.split(',') if t.strip()]
        if dino2.type in types_interdits:
            return False, f"{dino1.nom} n'aime pas les {dino2.type}s"

    if dino2.naime_pas_types:
        types_interdits = [t.strip() for t in dino2.naime_pas_types.split(',') if t.strip()]
        if dino1.type in types_interdits:
            return False, f"{dino2.nom} n'aime pas les {dino1.type}s"

    # 7. Vérifier les incompatibilités de famille
    if dino1.naime_pas_familles and dino2.famille:
        familles_interdites = [f.strip() for f in dino1.naime_pas_familles.split(',') if f.strip()]
        if dino2.famille in familles_interdites:
            return False, f"{dino1.nom} n'aime pas les {dino2.famille}"

    if dino2.naime_pas_familles and dino1.famille:
        familles_interdites = [f.strip() for f in dino2.naime_pas_familles.split(',') if f.strip()]
        if dino1.famille in familles_interdites:
            return False, f"{dino2.nom} n'aime pas les {dino1.famille}"

    # 8. Vérifier les compatibilités positives (bonus si défini)
    if dino1.aime.filter(id=dino2.id).exists():
        return True, f"{dino1.nom} apprécie {dino2.nom} !"
    if dino2.aime.filter(id=dino1.id).exists():
        return True, f"{dino2.nom} apprécie {dino1.nom} !"

    # Si aucune incompatibilité trouvée
    return True, "Compatible"


def get_compatibles(request, dino_ids):
    """
    API pour obtenir les dinosaures compatibles avec un ou plusieurs dinosaures sélectionnés
    dino_ids: chaîne d'IDs séparés par des virgules (ex: "1,3,5")
    """
    try:
        ids_list = [int(id.strip()) for id in dino_ids.split(',')]
        dinos_selectionnes = Dinosaure.objects.filter(id__in=ids_list)

        if not dinos_selectionnes.exists():
            return JsonResponse({'success': False, 'error': 'Aucun dinosaure trouvé'}, status=404)

        # Exclure les dinosaures déjà sélectionnés
        tous_les_dinos = Dinosaure.objects.exclude(id__in=ids_list)

        compatibles = []

        for dino in tous_les_dinos:
            # Vérifier la compatibilité avec TOUS les dinosaures de l'enclos
            est_compatible_avec_tous = True
            raisons = []

            for dino_enclos in dinos_selectionnes:
                est_compatible, raison = verifier_compatibilite(dino_enclos, dino)

                if not est_compatible:
                    est_compatible_avec_tous = False
                    raisons.append(raison)
                    break  # Pas besoin de vérifier les autres si déjà incompatible
                else:
                    if "apprécie" in raison:  # Relation positive
                        raisons.append(raison)

            # Ne garder que les dinosaures compatibles avec TOUS
            if est_compatible_avec_tous:
                compatibles.append({
                    'id': dino.id,
                    'nom': dino.nom,
                    'type': dino.type,
                    'famille': dino.famille or 'Non définie',
                    'image': dino.image.url if dino.image else None,
                    'raison': raisons[0] if raisons else 'Compatible'
                })

        return JsonResponse({
            'success': True,
            'dinos_selectionnes': [{
                'id': d.id,
                'nom': d.nom,
                'type': d.type,
                'famille': d.famille or 'Non définie',
                'image': d.image.url if d.image else None,
            } for d in dinos_selectionnes],
            'compatibles': compatibles,
            'count': len(compatibles)
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


