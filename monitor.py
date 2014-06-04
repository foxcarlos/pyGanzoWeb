import sys
import dbf
import bottle
from bottle import default_app, run, get, post, template
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket
from websocket import create_connection

users = set()

def llamar(pac):    
    ws = create_connection("ws://localhost:8080/websocket")
    
    #pac = raw_input('ingrese el paciente a llamar:')
    ws.send(pac)
    result =  ws.recv()
    print "Received '%s'" % result
    ws.close()

def buscarEnDbf(control):
    '''DBF Consultar la tabla especialidad que se encuentra en una tabla de VFP
    para obtner la descripcion de la especialidad y el telefono a donde se debe llamar'''

    #campo = 'file_dbf'
    #tabladbf = self.fc.get('RUTAS', campo)
    
    tabladbf = '/home/foxcarlos/desarrollo/python/pyGanzoWeb/static/file/dgtcabe.DBF'
    print tabladbf
    #tabladbf = archv_dbf
    try:
        tabla_especial = dbf.Table(tabladbf)
        tabla_especial.open()
    except:
        #self.logger.error('Error al abrir la tabla DBF')
        #sys.exit()
        pass

    #Buscar el codigo de la especialidad
    for reg in tabla_especial:
        devuelve = [] 
        if reg[1] == control:
            controlb = reg[1]
            tipo = reg[3]
            cedula = reg[4]
            nombre = reg[6]
            sexo = reg[11]
            edad = reg[12]
            return controlb, tipo, cedula, nombre, sexo, edad
        else:
            return devuelve

@get('/static/<filename:path>')
def static(filename): 
    return bottle.static_file(filename, root='static/')

@get('/')
def index():
    return template('index')

@get('/cliente')
def index2():
    return template('cliente')

@get('/llamados')
def llamados():
    return template('llamados3')

@get('/llamarPaciente')
def llamarPacienteGet():
    return template('quien_llama')

@post('/llamarPaciente')
def llamarPacientePost():
    ''' '''
    control = bottle.request.forms.get('control')
    print(control)
    l = buscarEnDbf(control)
    if l: 
        control, tipo, cedula, nombre, sexo, edad = l
        llamar(nombre)
        return template('quien_llama', {'control':control, 'tipo':tipo, 'cedula':cedula, 'nombre':nombre, 'sexo':sexo, 'edad':edad})
    else:
        return template('quien_llama')

@get('/websocket', apply=[websocket])
def chat(ws):
    print('entro en el metodo chat')
    users.add(ws)
    while True:
        msg = ws.receive()
        if msg is not None:
            for u in users:
                u.send(msg)
        else: break
    users.remove(ws)
   
run(host='0.0.0.0', port=8080, server=GeventWebSocketServer)
