from django import forms
from .models import Pricing, FixedCost, ProLabore


class PricingForm(forms.ModelForm):
    produtos_json = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Pricing
        fields = ['nome_cliente', 'tema_projeto', 'nome_precificacao', 'tempo_preparo', 'rendimento']


class FixedCostForm(forms.ModelForm):
    class Meta:
        model = FixedCost
        fields = ['descricao', 'valor_medio', 'valores']


class ProLaboreForm(forms.ModelForm):
    class Meta:
        model = ProLabore
        fields = ['descricao', 'valor_mensal']
