
# server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import querys
import os
import sett
import services
import json
app = Flask(__name__)
CORS(app)

@app.route('/webhook', methods=['GET'])
def verificar_token():
    try:
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if token == sett.token and challenge is not None:
            return challenge
        else:
            return 'Token incorrecto', 403
    except Exception as e:
        # Log detalles de la excepción para la depuración
        app.logger.error(f"Error en la función verificar_token: {str(e)}")
        return 'Error interno del servidor', 500
      

      
@app.route('/enviar_autorizacion_whats', methods=['POST'])
def enviar_primer_mensaje():
    data = request.json
    idsolicitud = data.get('idsolicitud')
    if not (idsolicitud):
        return jsonify({"error": "Falta el dato del idsolicitud."}), 400
    try:
        wa_solicitud = querys.get_solicitud(idsolicitud)
        detalle_lps=wa_solicitud[0][0]
        sucursal=wa_solicitud[0][1]  
        clave=wa_solicitud[0][2]
        text = detalle_lps
        options=["✅ Sí","❌ No"]
        mensaje = text.replace('<br>', '\n')
        body = ""
        body += f"\n- Clave: {clave}, Sucursal: {sucursal}, Mensaje: {mensaje} \n ¿Autorizas?"
        footer = "Pintacomex"
        numbers=querys.get_numeros(idsolicitud) 
        first=0
        print(numbers)
        for numb in numbers:
            
            #if first !=0:
            #    statuscheck=querys.check_status(idsolicitud)
            #    if statuscheck:
            #        break
            #    else:
            #        continue
            reply_button_data = services.buttonReply_Message(numb, options, body, footer, "sed1")
            response = services.enviar_Mensaje_whatsapp(reply_button_data)
            response_dict = json.loads(response.text)
            message_id = response_dict["messages"][0]["id"]
            print("ID del Mensaje:", message_id)
            querys.update_id_mensaje(message_id,idsolicitud,numb)
            first +=1
        # Convertir la cadena JSON en un diccionario
        return jsonify({"mensaje": f"Primer mensaje enviado correctamente.{response.text}"})
    except Exception as e:
        return jsonify({"error": "Error al enviar el mensaje: " + str(e)}), 500
      

      
@app.route('/webhook', methods=['POST'])
def recibir_mensajes():
    try:
        body = request.get_json()
        print(body)
        specific_id = body["entry"][0]["changes"][0]["value"]["messages"][0]["context"]["id"]
        print(specific_id)
        entry = body['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        message = value['messages'][0]
        number = services.replace_start(message['from'])
        title_value = body["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"]["button_reply"]["title"]
        querys.update_authorization_status(specific_id,title_value)
        return 'enviado'
    except Exception as e:
        print(e)
        return 'no enviado ' + str(e)

if __name__ == '__main__':
    app.run(debug=True)

