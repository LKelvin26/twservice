import mysql.connector

def connect_to_database():
    connection = mysql.connector.connect(
        host='104.225.220.243',
        user='sucursal',
        password='pdvr3P1iC@',
        database='sharedpinta'
    )
    return connection


def check_status(idsolicitud):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        query = "SELECT idSolicitud FROM wa_solicitudes  WHERE idsolicitud = %s "
        cursor.execute(query, (idsolicitud,))
        order_details = cursor.fetchall()
        if idsolicitud[0][0] == 0:
            status=False
        else:
            status=True
        return status
    except Exception as e:
        print(f"Error en get_order_details: {e}")

def get_solicitud(idsolicitud):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        query = "SELECT Mensaje,Sucursal,clave FROM wa_solicitudes  WHERE idsolicitud = %s "
        cursor.execute(query, (idsolicitud,))
        solicitud = cursor.fetchall()
        return solicitud
    except Exception as e:
        print(f"Error en get_order_details: {e}")

def get_numeros(idvsolicitud):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        query = "SELECT CelResponde FROM wa_validaciones  WHERE idsolicitud = %s "
        cursor.execute(query, (idvsolicitud,))
        numeros = cursor.fetchall()
        numeros = [item[0] for item in numeros]
        return numeros
    except Exception as e:
        print(f"Error en get_order_details: {e}")


        
def update_id_mensaje(idmensaje,idsolicitud,number):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        update_query = "UPDATE wa_validaciones SET idmensajeWA = %s  WHERE idSolicitud = %s and CelResponde=%s"
        cursor.execute(update_query, (idmensaje,idsolicitud,number,))
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
        update_query = "UPDATE wa_validaciones SET StatusWA = %s, FechaHoraAtencion = current_timestamp() WHERE idmensajeWA = %s and StatusWA=0"
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