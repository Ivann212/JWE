from django import forms
from .models import Dinosaure, Nourriture

class DinosaureAddForm(forms.ModelForm):
    class Meta:
        model = Dinosaure
        fields = ['nom', 'type', 'famille', 'nourriture', 'image']
        widgets = {
            'nourriture': forms.CheckboxSelectMultiple(attrs={'size': '3'})
        }


# Formulaire pour MODIFIER un dino (pour ajouter aime et n'aime pas)
class DinosaureEditForm(forms.ModelForm):
    class Meta:
        model = Dinosaure
        fields = ['aime', 'naime_pas', 'nom', 'type', 'famille', 'nourriture', 'image']
        widgets = {
            'nourriture': forms.CheckboxSelectMultiple(attrs={'size': '3'})
        }