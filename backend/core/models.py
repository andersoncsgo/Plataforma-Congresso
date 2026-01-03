from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. USUÁRIO PERSONALIZADO (Com CPF e Role)
class User(AbstractUser):
    ROLES_CHOICES = [
        ('USER', 'Usuário Padrão'),
        ('ADMIN', 'Administrador'),
    ]
    
    # O ID já é criado automaticamente pelo Django
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF")
    nome = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLES_CHOICES, default='USER')

    def __str__(self):
        return f"{self.username} - {self.nome}"

# 2. ROLES DE EVENTO (Tabela auxiliar)
class EventRole(models.Model):
    NOME_CHOICES = [
        ('ORGANIZADOR', 'Organizador'),
        ('COORGANIZADOR', 'Co-organizador'),
    ]
    nome = models.CharField(max_length=20, choices=NOME_CHOICES, unique=True)

    def __str__(self):
        return self.nome

# 3. EVENTOS
class Event(models.Model):
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
    ]

    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    data = models.DateField()
    local = models.CharField(max_length=255)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade_disponivel = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ativo')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

# 4. VÍNCULO USUÁRIO-EVENTO (Quem organiza o quê)
class UserEventRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_roles')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='team')
    role = models.ForeignKey(EventRole, on_delete=models.PROTECT)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Garante que um usuário não tenha funções duplicadas no mesmo evento
        unique_together = ('user', 'event', 'role')

# 5. COMPRAS
class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    data_compra = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Compra #{self.id} - {self.user.nome}"

# 6. INGRESSOS
class Ticket(models.Model):
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('utilizado', 'Utilizado'),
        ('cancelado', 'Cancelado'),
    ]

    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='tickets')
    codigo = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativo')

    def __str__(self):
        return f"Ticket {self.codigo}"