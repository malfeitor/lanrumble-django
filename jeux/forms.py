from django import forms
# from django.contrib.auth.models import User
from .models import Joueur, Jeu, Jeu_Societe


class ConfigColorsForm(forms.ModelForm):
    class Meta:
        model = Joueur
        exclude = ['utilisateur_id']
        fields = ['color_body_background', 'color_body_text', 'color_nav_background',
                  'color_nav_text', 'color_nav_link', 'color_nav_link_active',
                  'color_nav_link_hover', 'background_file']
        widgets = {
            'color_nav_link': forms.TextInput(attrs={'type': 'color'}),
            'color_nav_link_active': forms.TextInput(attrs={'type': 'color'}),
            'color_nav_link_hover': forms.TextInput(attrs={'type': 'color'}),
            'color_nav_text': forms.TextInput(attrs={'type': 'color'}),
            'color_nav_background': forms.TextInput(attrs={'type': 'color'}),
            'color_body_text': forms.TextInput(attrs={'type': 'color'}),
            'color_body_background': forms.TextInput(attrs={'type': 'color'}),
        }
        labels = {
            'color_nav_link': 'Navbar lien',
            'color_nav_link_active': 'Navbar ici',
            'color_nav_link_hover': 'Navbar lien survolé',
            'color_nav_text': 'Navbar texte',
            'color_nav_background': 'Navbar fond',
            'color_body_text': 'Texte de la page',
            'color_body_background': 'Fond de la page',
            'background_file': "Fond d'écran",
        }
