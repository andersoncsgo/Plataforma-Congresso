from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Event, EventRole, UserEventRole, Purchase, Ticket

# Configuração especial para o Usuário aparecer bonito no Admin
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Adicionamos 'cpf', 'telefone' e 'role' na visualização e na edição
    list_display = ('username', 'email', 'nome', 'cpf', 'role', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Pessoais', {'fields': ('cpf', 'nome', 'telefone', 'role')}),
    )

# Registro simples das outras tabelas
admin.site.register(Event)
admin.site.register(EventRole)
admin.site.register(UserEventRole)
admin.site.register(Purchase)
admin.site.register(Ticket)