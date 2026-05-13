from django import forms
from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'steps', 'preparation_time', 'difficulty', 'image', 'category', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre de la recette'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description'}),
            'ingredients': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Ingrédients (un par ligne)'}),
            'steps': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Étapes de préparation'}),
            'preparation_time': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Temps en minutes'}),
            'difficulty': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'tags': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }
