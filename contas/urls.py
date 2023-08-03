from django.contrib import admin
from django.urls import path
from .views import DespesasListView, relatorio_despesas , DespesasDeleteView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', DespesasListView.as_view(), name='lista_despesas'),
    path('relatorio/', relatorio_despesas, name='relatorio-despesas'),
    path('delete/<int:pk>/',DespesasDeleteView.as_view() , name='delete-despesas'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
