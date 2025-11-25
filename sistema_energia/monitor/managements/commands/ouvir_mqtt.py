import json
import paho.mqtt.client as mqtt
from django.core.management.base import BaseCommand
from monitor.models import Leitura

class Command(BaseCommand):
    help = 'Conecta no Mosquitto e salva dados no banco'

    def handle(self, *args, **kwargs):
        def on_message(client, userdata, msg):
            try:
                payload = msg.payload.decode('utf-8')
                print(f"Recebido: {payload}")
                dados = json.loads(payload)
                
                # Salva no Banco do Django
                Leitura.objects.create(
                    tensao=dados.get('tensao', 0),
                    corrente=dados.get('corrente', 0),
                    potencia=dados.get('potencia', 0)
                )
                print("--- Salvo no DB ---")
            except Exception as e:
                print(f"Erro: {e}")

        client = mqtt.Client()
        client.on_message = on_message
        
        print("Conectando ao Broker...")
        # Se seu broker tem senha, configure aqui. Se for local/anônimo, deixe assim.
        client.connect("127.0.0.1", 1883, 60)
        
        # O topico TEM que ser igual ao do ESP32
        client.subscribe("esp32/ina219")
        
        print("Esperando dados... (Pressione Ctrl+C para parar)")
        client.loop_forever()