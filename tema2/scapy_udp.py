from scapy.all import *
 
udp_layer = UDP()
udp_layer.sport = 54321
udp_layer.dport = 10000

ip_layer = IP()
ip_layer.src = '198.13.0.15'
ip_layer.dst = '198.13.0.14'

mesaj = Raw()
mesaj.load = "impachetat manual"

# folosim operatorul / pentru a stivui layerele
# sau pentru a adauga layerul cel mai din dreapta
# in sectiunea de date/payload a layerului din stanga sa
pachet_complet = ip_layer / udp_layer / mesaj

# trimitem fara a astepta un raspuns
send(pachet_complet)

# trimitem si inregristram raspunsurile
ans, unans = sr(pachet_complet, retry=3)
print ans
# <Results: TCP:0 UDP:1 ICMP:0 Other:0>

# ans contine o lista de tupluri [(request1, response1), (request2, response2)]
# raspunsul la primul requeste este mesajul primit de la server:
print ans[0][1]
# <IP  version=4L ihl=5L