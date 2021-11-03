import airshare
import requests
import socket
import webbrowser

SERVER_ADDR = 'http://172.30.1.48:32456'

CODE = 'brad-macbook-pro'
PORT = 23456

local_ip_addr = socket.inet_ntoa(airshare.utils.get_local_ip_address())

data = {
    'code': CODE,
    'ip_addr': local_ip_addr,
    'port': PORT,
}

r = requests.post('%s/register' % (SERVER_ADDR,), data)

print(r.json())

try:
    webbrowser.open('%s/browse' % SERVER_ADDR)
except:
    print('%s/browse' % SERVER_ADDR)

airshare.receiver.receive_server(code=CODE, port=PORT)
