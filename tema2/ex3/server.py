# TCP Server
from scapy.all import *
import socket
import logging
import time

logging.basicConfig(format=u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level=logging.NOTSET)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 11912
adresa = '198.13.0.14'
server_address = (adresa, port)
sock.bind(server_address)
logging.info("Serverul a pornit pe %s si portul %d", adresa, port)
sock.listen(1)
logging.info('Asteptam conexiuni...')
conexiune, address = sock.accept()
logging.info("S-a conectat cineva")
while True:
    data = conexiune.recv(1)
    if data == -1:
        break
    conexiune.send('A')
    logging.info('"%s"', data)

logging.info("Ending connection")

conexiune.close()
sock.close()
