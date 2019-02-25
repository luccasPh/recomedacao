from django import forms
from .models import Evento



class Evento_form(forms.ModelForm):
    data = forms.DateField(widget = forms.SelectDateWidget)
    class Meta:
        model = Evento
        fields = '__all__'
        labels = {
            'hr_ini': 'Horario Inicio:',
            'descricao': 'Descrição:',
            'data': 'Data:',
            'hr_fim': 'Horario Fim:',
            'priori': 'Priorizar evento'
        }
        widgets = {
            'descricao': forms.TextInput(
                attrs={'placeholder': 'Descrição do evento'}),
            'hr_ini': forms.TextInput(
                attrs={'placeholder': 'Horario de inicio do evento: H:M'}),
            'hr_fim': forms.TextInput(
                attrs={'placeholder': 'Horario do fim do evento: H:M'}),
        }