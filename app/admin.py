from django.contrib import admin
from . import models


@admin.register(models.Pricing)
class PricingAdmin(admin.ModelAdmin):
	list_display = ('nome_precificacao', 'nome_cliente', 'tema_projeto', 'data_pedido', 'created_by')
	search_fields = ('nome_precificacao', 'nome_cliente', 'tema_projeto')


@admin.register(models.FixedCost)
class FixedCostAdmin(admin.ModelAdmin):
	list_display = ('descricao', 'valor_medio')


@admin.register(models.ProLabore)
class ProLaboreAdmin(admin.ModelAdmin):
	list_display = ('descricao', 'valor_mensal')


@admin.register(models.History)
class HistoryAdmin(admin.ModelAdmin):
	list_display = ('timestamp', 'user', 'action', 'model_name', 'object_repr')
	readonly_fields = ('timestamp',)
