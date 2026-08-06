"""
Tests pour la logique de compatibilité entre dinosaures (jurassic_site/views.py).

Comment lancer ces tests :
    python manage.py test jurassic_site

Django va automatiquement chercher les classes qui héritent de TestCase
dans ce fichier, et exécuter chaque méthode qui commence par "test_".
"""

from django.test import TestCase
from .models import Dinosaure
from .views import verifier_compatibilite


class VerifierCompatibiliteTest(TestCase):
    # TestCase (et pas juste une classe Python normale) est important :
    # Django crée une base de données de test à part, exécute chaque
    # test dedans, puis ANNULE tout à la fin (rollback). Résultat :
    # tes tests ne touchent jamais ta vraie base de données, et un test
    # ne peut pas polluer le suivant.

    def test_carnivore_et_herbivore_incompatibles(self):
        # 1) ARRANGE : je prépare mes données.
        # On crée deux VRAIS objets Dinosaure en base de test (nécessaire
        # ici car verifier_compatibilite() appelle des méthodes comme
        # dino.naime_pas.all() ou dino.aime.filter(), qui ont besoin
        # d'un objet réellement sauvegardé pour fonctionner).
        rex = Dinosaure.objects.create(nom="T-Rex", type="Carnivore")
        tricera = Dinosaure.objects.create(nom="Tricératops", type="Herbivore")

        # 2) ACT : j'exécute la fonction que je veux tester.
        compatible, raison = verifier_compatibilite(rex, tricera)

        # 3) ASSERT : je vérifie que le résultat est celui attendu.
        # self.assertFalse(x) = "je m'attends à ce que x soit False"
        self.assertFalse(compatible)
        # self.assertIn(a, b) = "je m'attends à ce que a soit contenu dans b"
        self.assertIn("carnivores et herbivores", raison)

    # --- À toi de jouer ---
    #
    # Écris les tests suivants en suivant EXACTEMENT le même schéma
    # (Arrange / Act / Assert). Regarde verifier_compatibilite() dans
    # views.py pour connaître la règle à vérifier, ça t'aidera à choisir
    # les types de dinosaures à créer.
    #
    def test_deux_herbivores_sont_compatibles(self):
        tricera = Dinosaure.objects.create(nom="Tricératops", type="Herbivore")
        edmont = Dinosaure.objects.create(nom="Edmontosaure", type="Herbivore")

        compatible, raison = verifier_compatibilite(edmont, tricera)

        self.assertTrue(compatible)
        self.assertEqual(raison, "Compatible")
    #
    def test_reptile_marin_incompatible_avec_terrestre(self):
        mosa = Dinosaure.objects.create(nom="Mosasaure", type="Reptile marin")
        tricera = Dinosaure.objects.create(nom="Tricératops", type="Herbivore")

        compatible, raison = verifier_compatibilite(mosa, tricera)

        self.assertFalse(compatible)
        self.assertIn("enclos aquatique", raison)
    #
    def test_deux_reptiles_marins_sont_compatibles_entre_eux(self):
        mosa = Dinosaure.objects.create(nom="Mosasaure", type="Reptile marin")
        plesio = Dinosaure.objects.create(nom="Plésiosaure", type="Reptile marin")

        compatible, raison = verifier_compatibilite(mosa, plesio)

        self.assertTrue(compatible)
        self.assertEqual(raison, "Compatible")
    #
    def test_dino_qui_naime_pas_un_autre_individuellement(self):
        nasu = Dinosaure.objects.create(nom="Nasutocératops", type="Herbivore")
        penta = Dinosaure.objects.create(nom="Pentaceratops", type="Herbivore")
        nasu.naime_pas.add(penta)

        compatible, raison = verifier_compatibilite(penta, nasu)

        self.assertFalse(compatible)
        self.assertIn("n'aime pas", raison)

    def test_dino_incompatible_famille(self):
        anky = Dinosaure.objects.create(
            nom="Ankylosaure", type="Herbivore", famille="Ankylosauridé",
            naime_pas_familles="Sauropodes"
        )
        diplo = Dinosaure.objects.create(
            nom="Diplodocus", type="Herbivore", famille="Sauropodes"
        )

        # Sens 1 : anky.naime_pas_familles contre diplo.famille
        compatible, raison = verifier_compatibilite(anky, diplo)
        self.assertFalse(compatible)
        self.assertIn("n'aime pas les", raison)

        # Sens 2 : même données, ordre inversé → l'autre bloc du code est testé
        compatible2, raison2 = verifier_compatibilite(diplo, anky)
        self.assertFalse(compatible2)
        self.assertIn("n'aime pas les", raison2)
    #
    def test_deux_reptiles_volants_sont_compatibles_entre_eux(self):
        dimo = Dinosaure.objects.create(nom="Dimorphodon", type="Reptile volant")
        ptera = Dinosaure.objects.create(nom="Ptéranodon", type="Reptile volant")

        compatible, raison = verifier_compatibilite(ptera, dimo)

        self.assertTrue(compatible)
        self.assertEqual(raison, "Compatible")
    #
    def test_reptile_volant_incompatible_avec_terrestre(self):
        dimo = Dinosaure.objects.create(nom="Dimorphodon", type="Reptile volant")
        tricera = Dinosaure.objects.create(nom="Tricératops", type="Herbivore")

        compatible, raison = verifier_compatibilite(dimo, tricera)

        self.assertFalse(compatible)
        self.assertIn("une volière séparée", raison)
    #
    def test_reptile_volant_incompatible_avec_marin(self):
        dimo = Dinosaure.objects.create(nom="Dimorphodon", type="Reptile volant")
        mosa = Dinosaure.objects.create(nom="Mosasaure", type="Reptile marin")

        compatible, raison = verifier_compatibilite(dimo, mosa)

        # La règle "reptile marin" est vérifiée avant celle du "reptile
        # volant" dans le code : c'est donc elle qui se déclenche en premier.
        self.assertFalse(compatible)
        self.assertIn("enclos aquatique séparé", raison)
    #
    def test_piscivore_et_herbivore_incompatibles(self):
        spino = Dinosaure.objects.create(nom="Spinosaure", type="Piscivore")
        tricera = Dinosaure.objects.create(nom="Tricératops", type="Herbivore")

        compatible, raison = verifier_compatibilite(spino, tricera)

        self.assertFalse(compatible)
        self.assertIn("pas compatibles avec ce type", raison)
    #
    
    def test_piscivore_et_carnivore_incompatibles(self):
        spino = Dinosaure.objects.create(nom="Spinosaure", type="Piscivore")
        velo = Dinosaure.objects.create(nom="Velociraptor", type="Carnivore")

        compatible, raison = verifier_compatibilite(spino, velo)

        self.assertFalse(compatible)
        self.assertIn("pas compatibles avec ce type", raison)
    #

    def test_dino_qui_aime_un_autre_individuellement(self):
        diplo = Dinosaure.objects.create(nom="Diplodocus", type="Herbivore")
        galli = Dinosaure.objects.create(nom="Gallimimus", type="Herbivore")
        diplo.aime.add(galli)

        compatible, raison = verifier_compatibilite(diplo, galli)

        # "aime" est l'inverse de "naime_pas" : ça REND les dinos compatibles.
        self.assertTrue(compatible)
        self.assertIn("apprécie", raison)

        # Sens 2 : même données, ordre inversé → l'autre bloc du code est testé
        compatible2, raison2 = verifier_compatibilite(galli, diplo)
        self.assertTrue(compatible2)
        self.assertIn("apprécie", raison2)

    def test_naime_pas_type(self):
        trex = Dinosaure.objects.create(nom="tyranosaure", type="Carnivore", naime_pas_types="Carnivore")
        velo = Dinosaure.objects.create(nom="Velociraptor", type="Carnivore")
        
        compatible, raison = verifier_compatibilite(trex, velo)
        self.assertFalse(compatible)
        self.assertIn("n'aime pas les", raison)

        # Sens 1
        compatible, raison = verifier_compatibilite(trex, velo)
        self.assertFalse(compatible)
        self.assertIn("n'aime pas les", raison)

        # Sens 2 : même données, ordre inversé → l'autre bloc du code est testé
        compatible2, raison2 = verifier_compatibilite(velo, trex)
        self.assertFalse(compatible2)
        self.assertIn("n'aime pas les", raison2)