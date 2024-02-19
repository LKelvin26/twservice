from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse 

# Create your views here.

@csrf_exempt
def enviar_primer_mensaje(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        idsolicitud = data.get('idsolicitud')
        if not idsolicitud:
            return JsonResponse({"error": "Falta el dato del idsolicitud."}, status=400)
        try:
            # Tu lógica para enviar el primer mensaje
            return JsonResponse({"mensaje": "Primer mensaje enviado correctamente."})
        except Exception as e:
            return JsonResponse({"error": "Error al enviar el mensaje: " + str(e)}, status=500)

@csrf_exempt
def recibir_mensajes(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            # Tu lógica para procesar los mensajes recibidos
            return JsonResponse({"mensaje": "Mensaje recibido correctamente."})
        except Exception as e:
            return JsonResponse({"error": "Error al recibir el mensaje: " + str(e)}, status=500)
    else:
        return JsonResponse({"error": "Método no permitido"}, status=405)