from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Pricing, FixedCost, ProLabore, History
from .forms import PricingForm, FixedCostForm, ProLaboreForm
import json
from django import forms
from django.db import models


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
