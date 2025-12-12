

from django.db import models


class Nourriture(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name_plural = "Nourritures"


class Dinosaure(models.Model):
    TYPE_CHOICES = [
        ('Herbivore', 'Herbivore'),
        ('Carnivore', 'Carnivore'),
        ('Piscivore', 'Piscivore'),
        ('Reptile marin', 'Reptile marin'),
        ('Reptile volant', 'Reptile volant'),
    ]

    FAMILLE_CHOICES = [
        ('Sauropodes', 'Sauropodes'),
        ('Pachycéphalosauridé', 'Pachycéphalosauridé'),
        ('Hadrosauridé', 'Hadrosauridé'),
        ('Ankylosauridé', 'Ankylosauridé'),
        ('Cératopsien', 'Cératopsien'),
        ('Ornithomimosaurien', 'Ornithomimosaurien'),
        ('Charognard', 'Charognard'),
        ('Hybrides', 'Hybrides'),

    ]

    # Informations de base
    nom = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    famille = models.CharField(max_length=100, choices=FAMILLE_CHOICES, blank=True, null=True)  # ✅ Optionnel
    nourriture = models.ManyToManyField(Nourriture, blank=True)
    image = models.ImageField(upload_to='dinos/', blank=True, null=True)

    # Compatibilités individuelles
    aime = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='aimé_par')
    naime_pas = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='détesté_par')

    # Incompatibilités par catégories
    naime_pas_types = models.CharField(
        max_length=200,
        blank=True,
        help_text="Types incompatibles (séparés par des virgules)"
    )
    naime_pas_familles = models.CharField(
        max_length=200,
        blank=True,
        help_text="Familles incompatibles (séparées par des virgules)"
    )

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name_plural = "Dinosaures"
        ordering = ['nom']