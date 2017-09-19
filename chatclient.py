import socket
import sys
import argparse
from threading import Thread

# Create a UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Create a argument parser for command line arguments for username, server-ip and server-port
parser = argparse.ArgumentParser(description='Send correct to server')
parser.add_argument('-u', metavar='Username')
parser.add_argument('-sip', metavar='Server=ip')
parser.add_argument('-sp', metavar='Server Port')
args = parser.parse_args()

# Store the command line arguments into local variables
username = sys.argv[2]		
server_ip = sys.argv[4]
server_port = int(sys.argv[6])
msg = username

s.sendto(msg, (server_ip, server_port))

def send_message(data):
	users_contacted = {}
	msg = data.split(",")[0]
	username = msg.split()[0]
	message = " ".join(w for w in msg.split()[1:])
	addr = data.split(",")[1]
	addr_ip = addr.split(":")[0]
	addr_port = addr.split(":")[1]
	addr_port = int(addr_port)
	s.sendto(msg, (addr_ip, addr_port))
	return addr_ip, addr_port, username

def receive_message(data, addr, username):
	msg = username + "?"
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.sendto(msg,(server_ip, server_port))
	conn, add = sock.recvfrom(1000)
	sock.close()
	addr_ip = conn.split(":")[0]
	addr_port = conn.split(":")[1]
	msg = "From" + " " + addr_ip + ":" + addr_port + " " + username + " " + data.split(" ")[0]
	s.sendto(msg, addr) 
	
def data_receive():
	try:	
		while True:	
        		data, addr = s.recvfrom(1000) # Receive the data from the server
			if "," in data:
				send_message(data)
			elif addr == (server_ip, server_port):	
				print data
			elif ":" in data:
				print data
			else:
				username = data.split()[0]
				data = " ".join(w for w in data.split()[1:])
				print data
				receive_message(data, addr, username)
	except KeyboardInterrupt:
		print "Client is trying to close the connection ",username 
		sys.exit()

Thread(target=data_receive).start()

while True:
	#input = raw_input("<from IP:PORT:{}>".format(username))
	input = raw_input()
	if input == 'list' or input == 'List':
		s.sendto(input, (server_ip, server_port))
	else:
		s.sendto(input, (server_ip, server_port))     
