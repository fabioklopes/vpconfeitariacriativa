from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Pricing, FixedCost, ProLabore, History, FinishedRecipe, RecipeIngredient, Input
from .forms import PricingForm, FixedCostForm, ProLaboreForm, FinishedRecipeForm, RecipeIngredientForm, InputForm
import json
from django import forms
from django.db import models
from django.http import JsonResponse
from django.forms import inlineformset_factory


def home(request):
	# simple landing page
	return render(request, 'index.html')


@login_required
def pricing_list(request):
	q = request.GET.get('q', '')
	pricings = Pricing.objects.all().order_by('-data_pedido')
	if q:
		pricings = pricings.filter(
			models.Q(nome_cliente__icontains=q) |
			models.Q(tema_projeto__icontains=q) |
			models.Q(nome_precificacao__icontains=q)
		)
	return render(request, 'pricing_list.html', {'pricings': pricings, 'q': q})


@login_required
def pricing_create(request):
	if request.method == 'POST':
		form = PricingForm(request.POST)
		if form.is_valid():
			p = form.save(commit=False)
			produtos_json = request.POST.get('produtos_json', '[]')
			try:
				p.produtos = json.loads(produtos_json)
			except Exception:
				p.produtos = []
			p.created_by = request.user
			p.save()
			messages.success(request, 'Precificação salva.')
			return redirect('pricing_detail', pk=p.pk)
	else:
		form = PricingForm()
	return render(request, 'pricing_form.html', {'form': form})


@login_required
def pricing_detail(request, pk):
	p = get_object_or_404(Pricing, pk=pk)
	return render(request, 'pricing_detail.html', {'p': p})


@login_required
def costs_view(request):
	fixed_costs = FixedCost.objects.all()
	prolabore = ProLabore.objects.first()
	if request.method == 'POST':
		# simple handling to add new fixed cost
		form = FixedCostForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Custo fixo salvo.')
			return redirect('costs')
	else:
		form = FixedCostForm()
	return render(request, 'costs.html', {'fixed_costs': fixed_costs, 'prolabore': prolabore, 'form': form})


@login_required
def histories_view(request):
	logs = History.objects.all().order_by('-timestamp')[:200]
	return render(request, 'histories.html', {'logs': logs})


@login_required
def pricing_edit(request, pk):
	p = get_object_or_404(Pricing, pk=pk)
	if request.method == 'POST':
		form = PricingForm(request.POST, instance=p)
		if form.is_valid():
			p = form.save(commit=False)
			produtos_json = request.POST.get('produtos_json', '[]')
			try:
				p.produtos = json.loads(produtos_json)
			except Exception:
				p.produtos = []
			p.save()
			messages.success(request, 'Precificação atualizada.')
			return redirect('pricing_detail', pk=p.pk)
	else:
		form = PricingForm(instance=p)

	produtos_json = json.dumps(p.produtos or [])
	return render(request, 'pricing_form.html', {'form': form, 'produtos_json': produtos_json, 'editing': True, 'pricing': p})


@login_required
def finished_recipe_list(request):
    recipes = FinishedRecipe.objects.all()
    return render(request, 'finishedrecipe_list.html', {'recipes': recipes})


@login_required
def finished_recipe_detail(request, pk):
    recipe = get_object_or_404(FinishedRecipe, pk=pk)
    return render(request, 'finishedrecipe_detail.html', {'recipe': recipe})


@login_required
def finished_recipe_create(request):
    if request.method == 'POST':
        form = FinishedRecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            ingredients_json = request.POST.get('ingredients_json', '[]')
            
            total_cost = 0
            try:
                ingredients = json.loads(ingredients_json)
                for item in ingredients:
                    ingredient_id = item.get('ingredient_id')
                    quantity = float(item.get('quantity', 0))
                    if ingredient_id and quantity > 0:
                        ingredient = Input.objects.get(id=ingredient_id)
                        if ingredient.qtt_input > 0:
                            total_cost += (float(ingredient.unit_cost) / float(ingredient.qtt_input)) * quantity
            except (json.JSONDecodeError, TypeError):
                ingredients = []

            recipe.final_value = total_cost
            recipe.save()
            
            # Clear existing ingredients before adding new ones
            recipe.recipeingredient_set.all().delete()
            for item in ingredients:
                ingredient_id = item.get('ingredient_id')
                quantity = item.get('quantity')
                if ingredient_id and quantity:
                    ingredient = Input.objects.get(id=ingredient_id)
                    RecipeIngredient.objects.create(
                        recipe=recipe,
                        ingredient=ingredient,
                        quantity=quantity
                    )
            messages.success(request, 'Receita salva com sucesso!')
            return redirect('finished_recipe_detail', pk=recipe.pk)
    else:
        form = FinishedRecipeForm()
    
    inputs_for_js = []
    for input_obj in Input.objects.all():
        inputs_for_js.append({
            'id': input_obj.id,
            'name': input_obj.name,
            'unit_cost': str(input_obj.unit_cost),
            'unit_of_measurement': input_obj.unit_of_measurement,
            'qtt_input': str(input_obj.qtt_input)
        })

    return render(request, 'finishedrecipe_form.html', {'form': form, 'inputs': inputs_for_js})


@login_required
def finished_recipe_edit(request, pk):
    recipe = get_object_or_404(FinishedRecipe, pk=pk)
    if request.method == 'POST':
        form = FinishedRecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            recipe = form.save(commit=False)
            ingredients_json = request.POST.get('ingredients_json', '[]')
            
            total_cost = 0
            try:
                ingredients_data = json.loads(ingredients_json)
                for item in ingredients_data:
                    ingredient_id = item.get('ingredient_id')
                    quantity = float(item.get('quantity', 0))
                    if ingredient_id and quantity > 0:
                        ingredient = get_object_or_404(Input, id=ingredient_id)
                        if ingredient.qtt_input > 0:
                            total_cost += (float(ingredient.unit_cost) / float(ingredient.qtt_input)) * quantity
            except (json.JSONDecodeError, TypeError):
                ingredients_data = []

            recipe.final_value = total_cost
            recipe.save()

            # Clear existing ingredients
            recipe.recipeingredient_set.all().delete()
            
            # Add new ingredients
            for item in ingredients_data:
                ingredient_id = item.get('ingredient_id')
                quantity = item.get('quantity')
                if ingredient_id and quantity:
                    ingredient = get_object_or_404(Input, id=ingredient_id)
                    RecipeIngredient.objects.create(
                        recipe=recipe,
                        ingredient=ingredient,
                        quantity=quantity
                    )

            messages.success(request, 'Receita atualizada com sucesso!')
            return redirect('finished_recipe_detail', pk=recipe.pk)
    else:
        form = FinishedRecipeForm(instance=recipe)

    inputs_for_js = []
    for input_obj in Input.objects.all():
        inputs_for_js.append({
            'id': input_obj.id,
            'name': input_obj.name,
            'unit_cost': str(input_obj.unit_cost),
            'unit_of_measurement': input_obj.unit_of_measurement,
            'qtt_input': str(input_obj.qtt_input)
        })
        
    recipe_ingredients = recipe.recipeingredient_set.all()
    ingredients_json = json.dumps([
        {'ingredient_id': item.ingredient.id, 'quantity': float(item.quantity)}
        for item in recipe_ingredients
    ])

    return render(request, 'finishedrecipe_form.html', {
        'form': form,
        'recipe': recipe,
        'inputs': inputs_for_js,
        'ingredients_json': ingredients_json,
        'editing': True
    })


@login_required
def finished_recipe_delete(request, pk):
    recipe = get_object_or_404(FinishedRecipe, pk=pk)
    if request.method == 'POST':
        recipe.delete()
        messages.success(request, 'Receita excluída com sucesso!')
        return redirect('finished_recipe_list')
    return render(request, 'finishedrecipe_confirm_delete.html', {'recipe': recipe})


@login_required
def input_api_create(request):
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            input_obj = form.save()
            return JsonResponse({
                'id': input_obj.id,
                'name': input_obj.name,
                'qtt_input': str(input_obj.qtt_input),
                'unit_cost': str(input_obj.unit_cost),
                'unit_of_measurement': input_obj.unit_of_measurement,
            })
        return JsonResponse({'errors': form.errors}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
