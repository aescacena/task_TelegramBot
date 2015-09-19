__author__ = 'antonio'
# -*- coding: utf-8 -*-

import time
import telebot
from telebot import types
from datetime import date, datetime
import calendar, json
from apscheduler.schedulers.blocking import BlockingScheduler

'''
API_TOKEN = 'API_TOKEN'

bot = telebot.TeleBot(API_TOKEN)

# Handle '/start' and '/help'
@bot.message_handler(commands=['hola'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Temperatura', 'Led')
    msg = bot.reply_to(message, """\
Hola soy el bot de domotica.
Que desea realizar?
- Consultar Led
- Consultar temperatura
""", reply_markup=markup)
    bot.register_next_step_handler(msg, process_consulta_step)


def process_consulta_step(message):
    try:
        items = openhab.fetch_all_items('http://192.168.1.137:8080/rest')
        chat_id = message.chat.id
        consulta = message.text
        if (consulta == u'Temperatura'):
            temp = items.get('TestTemperature')
            bot.send_message(chat_id,temp.state)
        if (consulta == u'Led'):
            led = items.get('TestLed')
            bot.send_message(chat_id,led.state)
    except Exception as e:
        bot.reply_to(message, 'oooops')

bot.polling()

while True:
    time.sleep(1)
    pass
'''

API_TOKEN = '137531233:AAF2fu8D_lD14gqbJrgzVrDe0e5i3W4mzOw'

bot = telebot.TeleBot(API_TOKEN)
meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

user_dict = {}
id_antonio = 97129026
json_data = None
listaTareas = []


class dateObject:
    def __init__(self):
        self.ano = None
        self.mes = None
        self.dia = None

class tareas:
    def __init__(self):
        self.date = None
        self.dateEnd = None
        self.description = None
'''
Upgrade tasks stored in the JSON file to memory. A (listaTareas)
'''
def initializeObjectsTasks():
    try:
        with open('tareas.json') as json_file:
            json_data = json.load(json_file)

            if(json_data != None):
                for s in json_data:
                    nuevaTarea = tareas()
                    nuevaTarea.date = s['date']
                    nuevaTarea.dateEnd = s['dateEnd']
                    nuevaTarea.description = s['description']
                    listaTareas.append(nuevaTarea)

            else:
                print 'No hay tareas pendientes'

        json_file.close()

    except StandardError:
        print 'Fichero no existe'

def userPermitted(id):
    if(id == id_antonio):
        return True
    else:
        bot.send_message(id_antonio, 'No estas autorizado para esta operacion', reply_markup=None)
        return False

@bot.message_handler(commands=['editar'])
def deleteTask(message):
    if(userPermitted(message.chat.id)):
        showTasks(message)
        msg = bot.send_message(id_antonio, 'Elige el numero de tarea a editar', reply_markup=None)
        bot.register_next_step_handler(msg, selectAndEditTask)

def selectAndEditTask(message):
    if(listaTareas[int(message.text)-1] != None):
        user_dict[message.chat.id] = listaTareas[int(message.text)-1]
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add('Descripcion', 'Fecha')

        msg = bot.send_message(id_antonio, 'Que desea editar?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_edit_task)

    else:
        bot.send_message(id_antonio, 'Esta tarea no existe', reply_markup=None)

def process_edit_task(message):
    if(listaTareas[int(message.text)-1] != None):
        optionEdit = message.text
        #if optionEdit == u'Descripcion':
            #process_description_step(message)

        if optionEdit == u'Fecha':
            message.text='Si'
            process_date_end(message)


@bot.message_handler(commands=['eliminar'])
def deleteTask(message):
    if(userPermitted(message.chat.id)):
        showTasks(message)
        msg = bot.send_message(id_antonio, 'Elige el numero de tarea a elminar', reply_markup=None)
        bot.register_next_step_handler(msg, existsAndDeleteTask)

def existsAndDeleteTask(message):
    if(listaTareas[int(message.text)-1] != None):
        bot.send_message(id_antonio, 'Eliminado', reply_markup=None)
        del listaTareas[int(message.text)-1]
        addToFileJSON() #json file rewrite
    else:
        bot.send_message(id_antonio, 'Esta tarea no existe', reply_markup=None)
'''
JSON updates the file with all the tasks stored in memory. (listaTareas)
'''
def addToFileJSON():
    a_dict = []
    for tarea in listaTareas:
        cadena =  {
        "date": tarea.date,
        "dateEnd": tarea.dateEnd,
        "description": tarea.description
        }
        a_dict += [cadena]

    print a_dict
    with open('tareas.json', mode='w') as feedsjson:
        json.dump(a_dict, feedsjson)

    feedsjson.close()

@bot.message_handler(commands=['tareas'])
def showTasks(message):
    if(userPermitted(message.chat.id)):
        sTareas = """Estas son tus tareas. \n"""
        cont = 1
        for tarea in listaTareas:
            sTareas += "    "+str(cont) +" - "+tarea.description+"""\n"""
            cont+=1
        bot.send_message(id_antonio,sTareas)

@bot.message_handler(commands=['nueva'])
def send_welcome(message):
    if(userPermitted(message.chat.id)):
        bot.send_message(id_antonio,"""\
        Estas creando una alerta.
        /cancel: Para cancelar alerta
        """)

        msg = bot.send_message(id_antonio, 'Descripcion de la tarea', reply_markup=None)
        bot.register_next_step_handler(msg, process_description_step)

def process_description_step(message):
    try:
        chat_id = message.chat.id
        tarea = tareas()
        tarea.date = str(date.today().day) + '/' + str(date.today().month) + '/' + str(date.today().year)
        tarea.description = message.text
        user_dict[chat_id] = tarea

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add('Si', 'No')

        msg = bot.send_message(id_antonio, 'Tiene fecha limite la tarea?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_date_end)

    except Exception as e:
        bot.send_message(id_antonio, e.message)

def process_date_end(message):
    try:
        chat_id = message.chat.id
        limite = message.text
        if limite == u'Si':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            d = datetime.now()
            markup.add(str(d.year), str(d.year+1), str(d.year+2))

            msg = bot.send_message(id_antonio, 'Ano', reply_markup=markup)
            bot.register_next_step_handler(msg, process_ano_step)
        else:
            message.text = u'No'
            process_final_task(message)
    except Exception as e:
        bot.send_message(id_antonio, e.message)

def process_ano_step(message):
    try:
        chat_id = message.chat.id
        ano = message.text
        d = datetime.now()
        if not ano.isdigit():
            msg = bot.send_message(id_antonio, 'Debe ser numero, Ano?')
            bot.register_next_step_handler(msg, process_ano_step)
            return
        newDate = dateObject()
        newDate.ano = ano
        user_dict[chat_id+1] = newDate
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=3)
        if (int(ano) == d.year):
            for i in range(d.month-1, 12):
                markup.add(meses[i])
        else:
            markup.add(meses[0], meses[1], meses[2])
            markup.add(meses[3], meses[4], meses[5])
            markup.add(meses[6], meses[7], meses[8])
            markup.add(meses[9], meses[10], meses[11])

        msg = bot.send_message(id_antonio, 'Mes', reply_markup=markup)
        bot.register_next_step_handler(msg, process_mes_step,)
    except Exception as e:
        bot.send_message(id_antonio, 'oooops')

def getPosicionMes(mes):
    cont = 0
    for i in meses:
        if(i == mes):
            break
        cont = cont + 1
    return cont

def process_mes_step(message):
    try:
        chat_id = message.chat.id
        mes = message.text
        d = datetime.now()
        numeroMes = getPosicionMes(mes)
        newDate = user_dict[chat_id+1]
        newDate.mes = numeroMes+1
        ultimoDiaMes = calendar.monthrange(int(newDate.ano), int(newDate.mes))
        u = ultimoDiaMes[1]
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=3)

        if (newDate.mes == d.month):
            for i in range(d.day, u+1):
                markup.add(str(i))
        else:
            for i in range(1, u+1):
                markup.add(str(i))

        msg = bot.send_message(id_antonio, 'Dia', reply_markup=markup)
        bot.register_next_step_handler(msg, process_dia_step)
    except Exception as e:
        bot.send_message(id_antonio, e.message)

def process_dia_step(message):
    try:
        chat_id = message.chat.id
        dia = message.text
        if not dia.isdigit():
            msg = bot.send_message(id_antonio, 'Debe ser numero. Dia?')
            bot.register_next_step_handler(msg, process_dia_step)
            return
        newDate = user_dict[chat_id+1]
        newDate.dia = dia
        process_final_task(message)
    except Exception as e:
        bot.send_message(id_antonio, 'oooops')

def process_final_task(message):
    try:
        chat_id = message.chat.id
        tarea = user_dict[chat_id]

        if message.text == u'No':
            bot.send_message(chat_id, 'Tarea creada: \n' + 'Creada en: '+str(tarea.date) + '\n' + 'Descripcion: '+str(tarea.description))
        else:
            newDate = user_dict[chat_id+1]
            tarea.dateEnd =  str(newDate.dia) +'/' + str(newDate.mes) + '/' + str(newDate.ano)
            bot.send_message(chat_id, 'Tarea creada: \n' + 'Creada en: '+str(tarea.date) + '\n' + 'Caduca en: '+ str(tarea.dateEnd) + '\n' + 'Descripcion: '+str(tarea.description))

        listaTareas.append(tarea)
        addToFileJSON()

    except Exception as e:
        bot.send_message(id_antonio, e.message)

initializeObjectsTasks()
#addToFileJSON()
bot.polling()

#Para indicar en la parte superior del chat la accion que esta tomando el bot
#bot.send_chat_action(id_antonio,action='upload_photo')


while True:
    time.sleep(1)
    pass
