from django import forms
from django.utils import timezone
from .models import Game, Category


class GameForm(forms.ModelForm):

    class Meta:
        model = Game
        fields = ['name', 'release_date', 'category', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'release_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super(GameForm, self).__init__(*args, **kwargs)
        self.fields['category'].empty_label = None

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        if len(name) < 2:
            raise forms.ValidationError('name should be at least 2 characters.')
        return name
 
    def clean_description(self):
        description = self.cleaned_data.get('description', '')
        if not description:
            raise forms.ValidationError('description cannot be blank.')
        return description
 
    def clean_release_date(self):
        release_date = self.cleaned_data.get('release_date')
        if release_date and release_date > timezone.now().date():
            raise forms.ValidationError('Published date cannot be in the future.')
        return release_date
        
class ConfirmDeleteForm(forms.Form):
    confirm_title = forms.CharField(label='Type the game title to confirm', widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, game=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = game

    def clean_confirm_title(self):
        val = self.cleaned_data.get('confirm_title', '')
        if not self.game:
            raise forms.ValidationError('No game specified for confirmation.')
        if val.strip() != self.game.title:
            raise forms.ValidationError('Title does not match.')
        return val
