from django import template
register = template.Library()

#esse arquivo filtro.py deve ser registrado em settings.py em TEPLATES após options..
@register.filter(name="is_par")
def is_par(valor):
    """
    Funcção verifica se o número da linha da tabela empresa é par ou impar
    """
    return True if valor % 2 == 0 else False
        