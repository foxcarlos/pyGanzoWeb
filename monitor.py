import bottle
from bottle import default_app, run, get, post, template
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket

users = set()


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
    control = bottle.request.forms.get('control')
    print(control)
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
