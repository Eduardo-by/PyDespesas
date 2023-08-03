from django import forms
from .models import Despesas

class DespesaForm(forms.ModelForm):
    class Meta:
        model = Despesas
        fields = ['titulo', 'descricao', 'valor']
