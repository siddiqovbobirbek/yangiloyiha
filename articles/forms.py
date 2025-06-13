from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['izoh']
        widgets = {
            'izoh': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Izoh yozing...'}),
        }

