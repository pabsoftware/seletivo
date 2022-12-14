
from django.urls import path
from . import views

urlpatterns = [

    path('nova_empresa/', views.nova_empresa, name='nova_empresa'),
    path('empresas/', views.empresas, name='empresa'),
    path('excluir_empresas/<int:id>', views.excluir_empresa, name='excluir_empresa'),
    path('empresa/<int:id>', views.unica_empresa, name='unica_empresa'),
]

