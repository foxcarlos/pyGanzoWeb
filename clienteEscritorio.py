from websocket import create_connection
    
ws = create_connection("ws://localhost:8080/websocket")
print "Sending 'Hello, World'..."
pac = raw_input('ingrese el paciente a llamar:')
ws.send(pac)
print "Sent"
print "Reeiving..."
result =  ws.recv()
print "Received '%s'" % result
ws.close()