from django import forms
from .models import Dinosaure, Nourriture
from django_select2.forms import Select2MultipleWidget
class DinosaureAddForm(forms.ModelForm):
    class Meta:
        model = Dinosaure
        fields = ['nom', 'type', 'famille', 'nourriture', 'image']
        widgets = {
            'nourriture': forms.CheckboxSelectMultiple(attrs={'size': '3'})
        }



class DinosaureEditForm(forms.ModelForm):
    # Champs pour la sélection multiple
    naime_pas_types_select = forms.MultipleChoiceField(
        choices=Dinosaure.TYPE_CHOICES,
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'select2-multiple',
            'data-placeholder': 'Sélectionner des types incompatibles...'
        }),
        label="Types incompatibles"
    )

    naime_pas_familles_select = forms.MultipleChoiceField(
        choices=Dinosaure.FAMILLE_CHOICES,
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'select2-multiple',
            'data-placeholder': 'Sélectionner des familles incompatibles...'
        }),
        label="Familles incompatibles"
    )

    class Meta:
        model = Dinosaure
        fields = ['nom', 'type', 'famille', 'nourriture', 'image',
                  'aime', 'naime_pas']
        widgets = {
            'aime': forms.SelectMultiple(attrs={
                'class': 'select2-multiple',
                'data-placeholder': 'Dinosaures aimés...'
            }),
            'naime_pas': forms.SelectMultiple(attrs={
                'class': 'select2-multiple',
                'data-placeholder': 'Dinosaures détestés...'
            }),
            'nourriture': forms.SelectMultiple(attrs={
                'class': 'select2-multiple',
                'data-placeholder': 'Sélectionner la nourriture...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['aime'].queryset = Dinosaure.objects.exclude(pk=self.instance.pk)
            self.fields['naime_pas'].queryset = Dinosaure.objects.exclude(pk=self.instance.pk)

            # Pré-remplir les incompatibilités
            if self.instance.naime_pas_types:
                self.fields['naime_pas_types_select'].initial = self.instance.naime_pas_types.split(',')
            if self.instance.naime_pas_familles:
                self.fields['naime_pas_familles_select'].initial = self.instance.naime_pas_familles.split(',')

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Sauvegarder les incompatibilités
        instance.naime_pas_types = ','.join(self.cleaned_data['naime_pas_types_select'])
        instance.naime_pas_familles = ','.join(self.cleaned_data['naime_pas_familles_select'])

        if commit:
            instance.save()
            self.save_m2m()

        return instance