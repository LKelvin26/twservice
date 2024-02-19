import requests
import telegramAuto.sett as sett
import json
import time
from datetime import datetime, timedelta
import mysql.connector

def obtener_Mensaje_whatsapp(message):
    if 'type' not in message :
        text = 'mensaje no reconocido'
        return text

    typeMessage = message['type']
    if typeMessage == 'text':
        text = message['text']['body']
    elif typeMessage == 'button':
        text = message['button']['text']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'list_reply':
        text = message['interactive']['list_reply']['title']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'button_reply':
        text = message['interactive']['button_reply']['title']
    else:
        text = 'mensaje no procesado'
    
    
    return text

def enviar_Mensaje_whatsapp(data):
    try:
        whatsapp_token = sett.whatsapp_token
        whatsapp_url = sett.whatsapp_url
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer ' + whatsapp_token}
        response = requests.post(whatsapp_url, 
                                 headers=headers, 
                                data=data)
        print(response.status_code)
        print(response.text)
        if response.status_code == 200:
            return response
        else:
            return response.status_code
    except Exception as e:
        return e,403
    
def text_Message(number,text):
    data = json.dumps(
            {
                "messaging_product": "whatsapp",    
                "recipient_type": "individual",
                "to": number,
                "type": "text",
                "text": {
                    "body": text
                }
            }
    )
    return data

def buttonReply_Message(number, options, body, footer, sedd):
    buttons = []
    for i, option in enumerate(options):
        buttons.append(
            {
                "type": "reply",
                "reply": {
                    "id": sedd + "_btn_" + str(i+1),
                    "title": option
                }
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "buttons": buttons
                }
            }
        }
    )
    return data

def listReply_Message(number, options, body, footer, sedd,messageId):
    rows = []
    for i, option in enumerate(options):
        rows.append(
            {
                "id": sedd + "_row_" + str(i+1),
                "title": option,
                "description": ""
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "button": "Ver Opciones",
                    "sections": [
                        {
                            "title": "Secciones",
                            "rows": rows
                        }
                    ]
                }
            }
        }
    )
    return data

def document_Message(number, url, caption, filename):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "document",
            "document": {
                "link": url,
                "caption": caption,
                "filename": filename
            }
        }
    )
    return data

def sticker_Message(number, sticker_id):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "sticker",
            "sticker": {
                "id": sticker_id
            }
        }
    )
    return data

def get_media_id(media_name , media_type):
    media_id = ""
    if media_type == "sticker":
        media_id = sett.stickers.get(media_name, None)
    #elif media_type == "image":
    #    media_id = sett.images.get(media_name, None)
    #elif media_type == "video":
    #    media_id = sett.videos.get(media_name, None)
    #elif media_type == "audio":
    #    media_id = sett.audio.get(media_name, None)
    return media_id

def replyReaction_Message(number, messageId, emoji):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "reaction",
            "reaction": {
                "message_id": messageId,
                "emoji": emoji
            }
        }
    )
    return data

def replyText_Message(number, messageId, text):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "context": { "message_id": messageId },
            "type": "text",
            "text": {
                "body": text
            }
        }
    )
    return data

def markRead_Message(messageId):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id":  messageId
        }
    )
    return data
  
def connect_to_database():
    connection = mysql.connector.connect(
        host='104.225.220.243',
        user='sucursal',
        password='pdvr3P1iC@',
        database='sharedpinta'
    )
    return connection

def get_order_details(idvalidaciones):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        query = "SELECT mensaje,Sucursal,SolicitadaA,clave FROM wa_solicitudes  WHERE idvalidaciones = %s "
        cursor.execute(query, (idvalidaciones,))
        order_details = cursor.fetchall()
        return order_details
    except Exception as e:
        print(f"Error en get_order_details: {e}")
        
def update_id_mensaje(idmensaje,idvalidaciones,number):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        update_query = "UPDATE Validaciones SET idmensaje = %s  WHERE idvalidaciones = %s and CelResponde=%s"
        cursor.execute(update_query, (idmensaje,idvalidaciones,number,))
        connection.commit()
        
    except Exception as e:
        print(f"Error en update_authorization_status: {e}")
    finally:
        cursor.close()
        connection.close()
        
def update_authorization_status(idmensaje,seleccion):
    try:
        connection = connect_to_database()
        print("entra update")
        cursor = connection.cursor()
        if seleccion == "✅ Sí":
            auth = 1
        elif seleccion == "❌ No":  # Corregido 'else if' a 'elif' y arreglado error de sintaxis
            auth = 2
        else:
            auth = 3
        update_query = "UPDATE Validaciones SET StatusAutorizacion = %s, AutorizadaEn = 'WA', FechaHoraAutorizada = current_timestamp() WHERE idmensaje = %s and StatusAutorizacion=0"
        cursor.execute(update_query, (auth,idmensaje,))
        
        connection.commit()
    except Exception as e:
      print(f"Error en update_authorization_status: {e}")
      return e  # Devuelve la excepción para un manejo adicional si es necesario
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

def update_not_authorization_status(clave):
    try:
        
        connection = connect_to_database()
        
        cursor = connection.cursor()

        
        update_query = "UPDATE Validaciones SET StatusAutorizacion = 2, AutorizadaEn = 'WA', FechaHoraAutorizada = current_timestamp() WHERE clave = %s"
        cursor.execute(update_query, (clave,))
        
        connection.commit()
    except Exception as e:
        print(f"Error en update_authorization_status: {e}")
    finally:
        cursor.close()
        connection.close()
        
def administrar_chatbot(text, number, messageId, name):
    text = text.lower() #mensaje que envio el usuario
    list = []
    number = number[:2] + number[3:]
    print("numero del usuario", number)
    print("mensaje del usuario: ",text)
    markRead = markRead_Message(messageId)
    list.append(markRead)
    #time.sleep(2)
    
    if "hola" in text:
        #print(f'numero a buscar: {number}')
        order_details = get_order_details(number)
        print(f'ESTO ES ORDER DETAILS {order_details}')
        if order_details:
            
            body = "¡Hola! 👋 Se requiere autorización para el siguiente pedido:"
            mensaje_aplicado = False
            for row in order_details:
              if not mensaje_aplicado:
                  mensaje = row[2].replace('<br>', '\n')
                  body += f"\n- Clave: {row[0]}, Sucursal: {row[1]}, Mensaje: {mensaje} \n ¿Autorizas?"
                  mensaje_aplicado=True
            footer = "Equipo Pintacomex"
            options = ["✅ Sí", "❌ No"]

            reply_button_data = buttonReply_Message(number, options, body, footer, "sed1", messageId)
            reply_reaction = replyReaction_Message(number, messageId, "🫡")
            #listReplyData = listReply_Message(number, options, body, footer, "sed2", messageId)
            #data = text_Message(number,body)
            print(number)
            #list.append(data)
            #list.append(listReplyData)
            list.append(reply_reaction) 
            list.append(reply_button_data)
            print(list)

    elif "sí" in text:
      
        body = "¡Perfecto! La actualizacíon se realizará con éxito"
        #footer = "Equipo Pintacomex"
        
        order_id_to_authorize = None
        order_details = get_order_details(number)
        if order_details:
            order_id_to_authorize = order_details[0][0]  
        
        
        if order_id_to_authorize:
            update_authorization_status(order_id_to_authorize)
        listReplyData = text_Message(number, body)
        sticker = sticker_Message(number, get_media_id("perro_traje", "sticker"))

        list.append(listReplyData)
        list.append(sticker)
    elif "no" in text:
        body = "¡De acuerdo! La actualizacíon del rechazo se realizará con éxito"
          #footer = "Equipo Pintacomex"

        order_id_to_authorize = None
        order_details = get_order_details(number)
        if order_details:
          order_id_to_authorize = order_details[0][0]  


        if order_id_to_authorize:
          update_not_authorization_status(order_id_to_authorize)
        listReplyData = text_Message(number, body)
        #textMessage = text_Message(number,"¿Podrías darnos los detalles de tu pedido? 😊")
        list.append(listReplyData)
                                   
                                   
                                   
                                   
    elif "sí, envía el pdf" in text:
        sticker = sticker_Message(number, get_media_id("pelfet", "sticker"))
        textMessage = text_Message(number,"Genial, por favor espera un momento.")

        enviar_Mensaje_whatsapp(sticker)
        enviar_Mensaje_whatsapp(textMessage)
        time.sleep(3)

        document = document_Message(number, sett.document_url, "Listo 👍🏻", "Inteligencia de Negocio.pdf")
        enviar_Mensaje_whatsapp(document)
        time.sleep(3)

        body = "¿Te gustaría programar una reunión con uno de nuestros especialistas para discutir estos servicios más a fondo?"
        footer = "Equipo Pintacomex"
        options = ["✅ Sí, agenda reunión", "No, gracias." ]

        replyButtonData = buttonReply_Message(number, options, body, footer, "sed4",messageId)
        list.append(replyButtonData)
    elif "sí, agenda reunión" in text :
        body = "Estupendo. Por favor, selecciona una fecha y hora para la reunión:"
        footer = "Equipo Pintacomex"
        options = ["📅 10: mañana 10:00 AM", "📅 7 de junio, 2:00 PM", "📅 8 de junio, 4:00 PM"]

        listReply = listReply_Message(number, options, body, footer, "sed5",messageId)
        list.append(listReply)
    elif "7 de junio, 2:00 pm" in text:
        body = "Excelente, has seleccionado la reunión para el 7 de junio a las 2:00 PM. Te enviaré un recordatorio un día antes. ¿Necesitas ayuda con algo más hoy?"
        footer = "Equipo Pintacomex"
        options = ["✅ Sí, por favor", "❌ No, gracias."]


        buttonReply = buttonReply_Message(number, options, body, footer, "sed6",messageId)
        list.append(buttonReply)
    elif "no, gracias." in text:
        textMessage = text_Message(number,"Perfecto! No dudes en contactarnos si tienes más preguntas. Recuerda que también ofrecemos material gratuito para la comunidad. ¡Hasta luego! 😊")
        list.append(textMessage)
    else :
        data = text_Message(number,"Lo siento, no estoy funcionandoa")
        print(number)
        list.append(data)

    for item in list:
        enviar_Mensaje_whatsapp(item)

#al parecer para mexico, whatsapp agrega 521 como prefijo en lugar de 52,
# este codigo soluciona ese inconveniente.
def replace_start(s):
    if s.startswith("521"):
        return "52" + s[3:]
    else:
        return s

# para argentina
def replace_start(s):
    if s.startswith("549"):
        return "54" + s[3:]
    else:
        return s
