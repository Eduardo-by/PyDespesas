from celery import shared_task
from datetime import datetime, timedelta
from .models import Caixa

@shared_task
def verificar_abertura_caixa():
    agora = datetime.now()
    data_anterior = agora - timedelta(days=1)
    
    if Caixa.objects.filter(data=data_anterior).exists():
        # Caixa do dia anterior já existe, abra um novo caixa
        novo_caixa = Caixa.objects.create()
        return f"Novo caixa aberto para {agora.date()}: {novo_caixa}"
    
    return f"Não foi necessário abrir um novo caixa para {agora.date()}"
