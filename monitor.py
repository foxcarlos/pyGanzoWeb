import bottle
from bottle import default_app, run, get, template
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
def index():
    return template('cliente')

@get('/llamados')
def index():
    return template('llamados')
    
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
