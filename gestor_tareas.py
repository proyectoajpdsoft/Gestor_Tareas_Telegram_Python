# ProyectoA (https://www.proyectoa.com)
# Gestor de Tareas (To-Do List) para Telegram
# Versión 1.0

import json
import requests
import time
import urllib
from bd import BD
import datetime
from datetime import date
from datetime import timedelta

# Bot real en Telegram creado para este tutorial por ProyectoA: GestorDeTareas_Bot
TOKEN_BOT_TODOLIST = "71739:AN4CqQk34Y6HDAYSr"

# La URL generada tendrá el formato:
# https://api.telegram.org/bot971:ACcVf7cxw5/getUpdates
URL = "https://api.telegram.org/bot{}/".format(TOKEN_BOT_TODOLIST)

# Establecemos los comandos que reconocerá el Bot de Telegram
comando_eliminar = ("eliminar", "borrar", "suprimir")
comando_inicio = ("inicio", "iniciar", "start")
comando_ayuda = ("ayuda", "help", "info", "comandos")
comando_nueva = ("añadir", "nueva", "insertar", "tarea", "task", "new")
comando_mostrar_todas = ("todas", "todos", "resueltas", "resueltos", "mostrar_todas", "mostrar_todos", "mostrar-todas", 
                     "mostrar.todas", "listar.todas","lista.todas", "ver.todas", "ver-todas", "all")
comando_mostrar_no_resueltas = ("lista", "listar", "mostrar", "tareas", "ver", "list")
comando_resolver = ("resolver", "finalizar", "completar", "fin", "end", "solved")
comando_reabrir = ("reabrir", "abrir", "open")
comando_mostrar_dias = ("pendientes", "dias", "pendiente", "restantes", "restante")

# Instanciamos la clase BD para acceso a SQLite
db = BD()

# Obtener el contenido HTML de una URL
def obtenerContenidoURL(url):
    respuesta = requests.get(url)
    contenido = respuesta.content.decode("utf8")
    return contenido

# Obtener el contenido en JSON de una URL
def obtenerJSONURL(url):
    contenido = obtenerContenidoURL(url)
    contenidoJSON = json.loads(contenido)
    return contenidoJSON

# Obtener los últimos mensajes no leídos en Bot de Telegram en formato JSON
def obtenerUltimosMensajes(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    contenidoJSON = obtenerJSONURL(url)
    return contenidoJSON

# Obtener el ID del úlitmo update del getUpdates (obtenerUltimosMensajes)
def obtenerUltimoIDUpdate(updates):
    UpdateID = []
    for update in updates["result"]:
        UpdateID.append(int(update["update_id"]))
    return max(UpdateID)

# Obtenemos los mensajes y ejecutar el comando correspondiente
# eliminar, insertar, listar, ayuda, resolver, reabrir, inicio
def obtenerMensajeEjecutarComando(updates):
    textoRecibo = ""
    for update in updates["result"]:
        try:
            textoRecibo = update["message"]["text"]
            # Mostramos en cosola para depuración
            print("Texto leído: " + textoRecibo)
        except Exception as e:
            print(e)
            pass
        try:
            chat = update["message"]["chat"]["id"]
        except Exception as e:
            print(e)
            pass
        
        # Si se ha introducido una barra / se quita para comparar los comandos
        if textoRecibo.startswith("/"):
            textoRecibo = textoRecibo[1:]
            
        # Eliminar tarea (eliminar codigo_tarea)    
        if textoRecibo.lower().startswith(comando_eliminar):
            # Obtenemos el comando y el código de la tarea (separados por espacio)
            textoDividido = textoRecibo.split(" ")
            if len(textoDividido) < 2:
                enviarMensajeAChat(texto="Envía: eliminar codigo_tarea", idChat=chat)
            else:
                codigo = textoDividido[1]
                tarea = db.obtenerTareaCodigo(codigo=codigo, autor=chat)
                if tarea == None:
                    enviarMensajeAChat(texto=f"No se ha encontrado la tarea con código {codigo}", idChat=chat)
                else:
                    db.eliminarTarea(codigo=codigo, autor=chat)
                    enviarMensajeAChat(texto="La tarea " + codigo + " ha sido eliminada correctamente", idChat=chat)
                    
        # Resolver tarea (resolver codigo_tarea)
        if textoRecibo.lower().startswith(comando_resolver):
            # Obtenemos el comando y el código de la tarea (separados por espacio)
            textoDividido = textoRecibo.split(" ")
            if len(textoDividido) < 2:
                enviarMensajeAChat(texto="Envía: resolve codigo_tarea", idChat=chat)
            else:
                codigo = textoDividido[1]
                tarea = db.obtenerTareaCodigo(codigo=codigo, autor=chat)
                if tarea == None:
                    enviarMensajeAChat(texto=f"No se ha encontrado la tarea con código {codigo}", idChat=chat)
                else:
                    db.resolverTarea(codigo=codigo, autor=chat)
                    enviarMensajeAChat(texto="La tarea " + codigo + " ha sido resuelta correctamente", idChat=chat)
        
        # Reabrir tarea resuelta (reabrir codigo_tarea)
        if textoRecibo.lower().startswith(comando_reabrir):
            # Obtenemos el comando y el código de la tarea (separados por espacio)
            textoDividido = textoRecibo.split(" ")
            if len(textoDividido) < 2:
                enviarMensajeAChat(texto="Envía: reabrir codigo_tarea", idChat=chat)
            else:
                codigo = textoDividido[1]
                tarea = db.obtenerTareaCodigo(codigo=codigo, autor=chat)
                if tarea == None:
                    enviarMensajeAChat(texto=f"No se ha encontrado la tarea con código {codigo}", idChat=chat)
                else:
                    db.reabrirTarea(codigo=codigo, autor=chat)
                    enviarMensajeAChat(texto="La tarea " + codigo + " ha sido reabierta correctamente", idChat=chat)                    
        elif textoRecibo.lower().startswith(comando_inicio):
            enviarMensajeAChat(texto="Envía: 'ayuda' para mostrar los comandos que el bot reconoce.", idChat=chat)
        elif textoRecibo.lower().startswith(comando_ayuda):
            comando1 = "<b>añadir..tarea..fecha</b> (dd-mm-aaaa) → Añadir una tarea"
            comando2 = "\n\n<b>tareas</b> → Mostrar tareas sin resolver"
            comando3 = "\n\n<b>pendientes</b> → Mostrar sin resolver con días pendientes"
            comando4 = "\n\n<b>todas</b> → Mostrar todas las tareas"
            comando5 = "\n\n<b>eliminar codigo_tarea</b> → Eliminar una tarea"
            comando6 = "\n\n<b>resolver codigo_tarea</b> → Resolver una tarea"
            comando7 = "\n\n<b>reabrir codigo_tarea</b> → Reabrir tarea resuelta"
            comando8 = "\n\n<b>ayuda</b> → Muestra los comandos reconocidos"
            mensaje = comando1 + comando2 + comando3 + comando4 + comando5 + comando6 + comando7 + comando8
            enviarMensajeAChat(texto=mensaje, idChat=chat)
        elif textoRecibo.lower().startswith(comando_mostrar_no_resueltas):
            tareas = db.obtenerTareas(chat)
            if tareas == []:
                enviarMensajeAChat(texto="No hay tareas sin resolver para mostrar.", idChat=chat)
            for i in range(len(tareas)):
                codigo = tareas[i][0]
                tarea = tareas[i][1]
                fecha = tareas[i][2]
                mensaje = f"{codigo} {tarea} {fecha}"
                enviarMensajeAChat(texto=mensaje, idChat=chat)
        elif textoRecibo.lower().startswith(comando_mostrar_todas):
            tareas = db.obtenerTareasTodas(chat)
            if tareas == []:
                enviarMensajeAChat("No hay tareas para mostrar.", chat)
            for i in range(len(tareas)):               
                codigo = tareas[i][0]
                tarea = tareas[i][1]
                fecha = tareas[i][2]
                resuelta = tareas[i][3]
                if (resuelta == 1):
                    mensaje = f"{codigo} <s>{tarea}</s> {fecha}"
                else:
                    mensaje = f"{codigo} {tarea} {fecha}"
                enviarMensajeAChat(texto=mensaje, idChat=chat)
        elif textoRecibo.lower().startswith(comando_mostrar_dias):
            # Obtenemos las tareas sin resolver
            tareas = db.obtenerTareas(chat)
            if tareas == []:
                enviarMensajeAChat("No hay tareas pendientes de resolver para mostrar.", chat)
            else:
                fechaHoy = datetime.datetime.today()
                for i in range(0, len(tareas)):
                    try:
                        codigo = tareas[i][0]
                        texto = tareas[i][1]
                        fechaTarea = tareas[i][2]
                        fechaTareaFormato = datetime.datetime.strptime(fechaTarea, "%d-%m-%Y")                        
                        fechaHoyFormato = datetime.datetime(year=fechaHoy.year, month=fechaHoy.month, day=fechaHoy.day)
                        diferencia = fechaTareaFormato - fechaHoyFormato
                        dias = diferencia.days
                        if dias > 1:
                            mensajeDias = "quedan " + str(dias) + " días"
                        elif dias == 1:
                            mensajeDias = "queda 1 día"
                        else:
                            mensajeDias = "fecha anterior"
                        mensaje = str(codigo) + " " + texto + " → " + mensajeDias
                        enviarMensajeAChat(texto=mensaje, idChat=chat)
                    except:
                        mensaje = f"Error al obtener la fecha de la tarea con código {tareas[i][0]}"
                        enviarMensajeAChat(texto=mensaje, idChat=chat)
                        pass                    
        elif textoRecibo.lower().startswith(comando_nueva):
            # Usamos el separador ".." para obtener el texto de la tarea y la fecha
            textoDividido = textoRecibo.split("..")
            if len(textoDividido) < 3:
                enviarMensajeAChat(texto="Envía: añadir..tarea..fecha (formato dd-mm-aaaa)", idChat=chat)
            elif len(textoDividido[1]) < 1 or len(textoDividido[2]) < 1:
                enviarMensajeAChat(texto="Envía: añadir..tarea..fecha (formato dd-mm-aaaa)", idChat=chat)
            else:                
                texto = textoDividido[1]
                fecha = textoDividido[2]
                db.insertarTarea(tarea=texto, fecha=fecha, autor=chat, resuelta=0)
                enviarMensajeAChat(texto="Tarea <i>" + texto + "</i> insertada correctamente", idChat=chat)        
        else:
            # Si existe la variable "chat"
            if "chat" in locals():
                mensaje = f"No reconozco el comando <i>{textoRecibo}</i>, Envía: 'ayuda' para mostrarte los comandos que reconozco"
                enviarMensajeAChat(texto=mensaje, idChat=chat)
            else: # Si ha habido algún error y no existe la variable "chat"
                print("Error al obtener el ID del chat")

# Obtiene el ID del chat del que recibe el texto y también el propio texto enviado
def obtenerChatIDyTexto(updates):
    numUpdates = len(updates["result"])
    ultimoUpdate = numUpdates - 1
    texto = updates["result"][ultimoUpdate]["message"]["text"]
    idChat = updates["result"][ultimoUpdate]["message"]["chat"]["id"]
    return texto, idChat

# Envía un mensaje al chat indicado de Telegram
def enviarMensajeAChat(texto, idChat, formato=None):
    # Limpiamos el texto de cualquier carácter no permitido
    texto = urllib.parse.quote_plus(texto)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=HTML".format(texto, idChat)
    if formato:
        url += "&reply_markup={}".format(formato)
    obtenerContenidoURL(url)

# Procedimiento principal de inicio de aplicación
def main():
    # Creamos la base de datos SQLite y la tabla "tareas" (si no existe)
    db.crearBD()
    idUltimoUpdate = None
    # Ejeuctamos un bucle infinito para manter la aplicación siempre abierta
    # Comprobamos si hay nuevos mensajes por leer en el Bot
    while True:
        updates = obtenerUltimosMensajes(idUltimoUpdate)
        if len(updates["result"]) > 0:
            idUltimoUpdate = obtenerUltimoIDUpdate(updates) + 1
            obtenerMensajeEjecutarComando(updates)
        time.sleep(0.5)

# Llamamos al procedimiento principal
if __name__ == '__main__':
    main()