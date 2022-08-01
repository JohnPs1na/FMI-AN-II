import socket
import logging
import time

logging.basicConfig(format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.NOTSET)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)

port = 10044
adresa = "198.10.0.2"
server_address = (adresa, port)
sock.bind(server_address)
logging.info("Serverul a pornit pe %s si portul %d", adresa, port)
sock.listen(5)
conexiune = None
while conexiune == None:
    logging.info('Asteptam conexiui...')
    conexiune, address = sock.accept()
    logging.info("Handshake cu %s", address)

msg = []
while True:
    try:
        data = conexiune.recv(1024)
        logging.info('Content primit: "%s"', data)
        msg.append(data)
        conexiune.send("ACCEPT".encode('utf-8'))
        if len(msg) > 8:
            break
    except KeyboardInterrupt:
        print("\nCtrl + C pressed.............Exiting")
        logging.info('closing socket')
        poza = b''.join(msg)
        with open('poza_server.png','wb') as g:
            g.write(poza)
        conexiune.close()
        sock.close()
        exit()

poza = b''.join(msg)
with open('poza_server.png','wb') as g:
    g.write(poza)