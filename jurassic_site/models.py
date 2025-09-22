from django.db import models


class Nourriture(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nom


class Dinosaure(models.Model):
    TYPE_CHOICES = [
        ('Herbivore', 'Herbivore'),
        ('Carnivore', 'Carnivore'),
        ('Piscivore', 'Piscivore'),
        ('Reptile marin', 'Reptile marin'),
        ('Reptile volant', 'Reptile volant'),
    ]

    nom = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    famille = models.CharField(max_length=100, blank=True)

    nourriture = models.ManyToManyField(Nourriture, blank=True)

    aime = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='aimé_par')
    naime_pas = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='détesté_par')

    image = models.ImageField(upload_to='dinos/', blank=True, null=True)

    def __str__(self):
        return self.nom

