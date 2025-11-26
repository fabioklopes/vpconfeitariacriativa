from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

# Use Django's user model
User = get_user_model()


class Pricing(models.Model):
	nome_cliente = models.CharField(max_length=80)
	data_pedido = models.DateTimeField(auto_now_add=True)
	tema_projeto = models.CharField(max_length=80)
	nome_precificacao = models.CharField(max_length=120, default='')
	produtos = models.JSONField(default=list, blank=True)
	tempo_preparo = models.IntegerField(default=0, help_text='Tempo em minutos')
	rendimento = models.CharField(max_length=80, blank=True, default='')
	created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='pricings')

	def tempo_human(self):
		# convert minutes to H:M
		mins = self.tempo_preparo
		hours = mins // 60
		minutes = mins % 60
		if hours:
			return f"{hours}h {minutes}m"
		return f"{minutes}m"

	def __str__(self):
		return f"{self.nome_precificacao} - {self.nome_cliente}"


class FixedCost(models.Model):
	descricao = models.CharField(max_length=120)
	valores = models.JSONField(default=dict, blank=True, help_text='Valores flexíveis em JSON')
	valor_medio = models.DecimalField(max_digits=12, decimal_places=2, default=0)

	def total_mensal(self):
		return float(self.valor_medio)

	def total_diario(self):
		return float(self.valor_medio) / 30

	def total_hora(self):
		return self.total_diario() / 24

	def total_minuto(self):
		return self.total_hora() / 60

	def __str__(self):
		return self.descricao


class ProLabore(models.Model):
	descricao = models.CharField(max_length=120, default='Pró-labore')
	valor_mensal = models.DecimalField(max_digits=12, decimal_places=2, default=0)

	class Meta:
		verbose_name = "Pró-labore"
		verbose_name_plural = "Pró-labores"

	def ganho_diario(self):
		return float(self.valor_mensal) / 30

	def ganho_hora(self):
		return self.ganho_diario() / 24

	def ganho_minuto(self):
		return self.ganho_hora() / 60

	def __str__(self):
		return self.descricao


class History(models.Model):
	ACTIONS = (("create", "create"), ("update", "update"), ("delete", "delete"))
	user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
	action = models.CharField(max_length=10, choices=ACTIONS)
	model_name = models.CharField(max_length=120)
	object_repr = models.CharField(max_length=255)
	timestamp = models.DateTimeField(default=timezone.now)
	changes = models.JSONField(default=dict, blank=True)

	def __str__(self):
		return f"[{self.timestamp}] {self.user} {self.action} {self.model_name} -> {self.object_repr}"


class Input(models.Model):
	MEASUREMENTS =(("litro", "Litro"), ("unidade", "Unidade"), ("quilo", "Quilo"), ("metro", "Metro"))
	name = models.CharField(max_length=80, verbose_name="Produto") 
	qtt_input = models.DecimalField(max_digits=12, decimal_places=3, default=0, verbose_name="Quantidade do Insumo")
	unit_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Custo Unitário") 
	unit_of_measurement = models.CharField(max_length=25, choices=MEASUREMENTS, verbose_name="Unidade de Medida")
	last_updated = models.DateTimeField(auto_now=True, verbose_name="Ultima Atualização")

	class Meta:
		verbose_name = "Insumo"
		verbose_name_plural = "Insumos"
		ordering = ["name"]

	def __str__(self):
		return self.name


class FinishedRecipe(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome da Receita")
    
    YIELD_UNITS = (
        ("unidades", "Unidades"),
        ("quilo", "Quilo"),
    )
    yield_unit = models.CharField(max_length=10, choices=YIELD_UNITS, verbose_name="Unidade de Rendimento")
    yield_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Rendimento")
    
    ingredients = models.ManyToManyField('Input', through='RecipeIngredient', related_name='recipes', verbose_name="Ingredientes")
    
    preparation_time = models.PositiveIntegerField(verbose_name="Tempo de Preparo (minutos)")
    final_value = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Valor Final da Receita")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Receita Pronta"
        verbose_name_plural = "Receitas Prontas"


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(FinishedRecipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey('Input', on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Quantidade")

    def __str__(self):
        return f"{self.quantity} of {self.ingredient.name} for {self.recipe.name}"

    class Meta:
        verbose_name = "Ingrediente da Receita"
        verbose_name_plural = "Ingredientes da Receita"
        unique_together = ('recipe', 'ingredient')