# inainte de toate trebuie adaugata o regula de ignorare 
# a pachetelor RST pe care ni le livreaza kernelul automat
# iptables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP
from scapy.all import *
import socket
import logging
import time


logging.basicConfig(format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.NOTSET)

ip = IP()
ip.src = '198.13.0.15'
ip.dst = '198.13.0.14'
tcp = TCP()
tcp.sport = 6969
tcp.dport = 11912
tcp.seq = 100
tcp.flags = 'S'

SYN = ip/tcp
raspuns_SYN_ACK = sr1(SYN)

tcp.seq += 1
tcp.ack = raspuns_SYN_ACK.seq + 1
tcp.flags = 'A'

ACK = ip / tcp
send (ACK)

logging.info("Am terminat handshake-ul")

options = [('MSS',2)]
ip.tos = int('011110' + '11', 2)


for ch in "abc":
    tcp.flags = 'PACE'
    tcp.ack = raspuns_SYN_ACK.seq + 1
    rcv = sr1(ip/tcp/ch, timeout=2, verbose=0)
    rcv.show()
    tcp.seq += 1

tcp.ack = raspuns_SYN_ACK.seq + 1
rcv = sr1(ip/tcp/'abc')
rcv.show()

tcp.flags = 'R'
rcv = sr1(ip/tcp)
rcv.show()

tcp.flags = 'PACE'
tcp.ack = raspuns_SYN_ACK.seq + 1
rcv = sr1(ip/tcp/'a')
rcv.show()

logging.info("Se incheie conexiunea")


