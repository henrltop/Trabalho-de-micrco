from django.shortcuts import render
from .models import Leitura
from django.utils import timezone
from datetime import timedelta

def index(request):
    ultima = Leitura.objects.last()
    
    status_online = False
    
    if ultima:
        # Pega a hora atual (com fuso horário correto do Django)
        agora = timezone.now()
        
        # Calcula a diferença de tempo
        diferenca = agora - ultima.data_hora
        
        # Se a última mensagem foi há menos de 10 segundos, está ONLINE
        if diferenca < timedelta(seconds=10):
            status_online = True

    return render(request, 'index.html', {
        'leitura': ultima,
        'online': status_online
    })