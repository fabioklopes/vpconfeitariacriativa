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


@admin.register(models.Input)
class InputAdmin(admin.ModelAdmin):
	list_display = ('name', 'qtt_input', 'unit_cost', 'unit_of_measurement', 'last_updated')
	search_fields = ('name',)
	readonly_fields = ('last_updated',)


@admin.register(models.FinishedRecipe)
class FinishedRecipeAdmin(admin.ModelAdmin):
	list_display = ('name', 'yield_unit', 'yield_amount', 'preparation_time', 'final_value')
	search_fields = ('name',)
	