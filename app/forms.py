from django import forms
from .models import Pricing, FixedCost, ProLabore, FinishedRecipe, RecipeIngredient, Input


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


class FinishedRecipeForm(forms.ModelForm):
    class Meta:
        model = FinishedRecipe
        fields = ['name', 'yield_unit', 'yield_amount', 'preparation_time']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'yield_unit': forms.Select(attrs={'class': 'form-select'}),
            'yield_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'preparation_time': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'quantity']


class InputForm(forms.ModelForm):
    class Meta:
        model = Input
        fields = ['name', 'qtt_input', 'unit_cost', 'unit_of_measurement']
