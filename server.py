import socket
import sys
from thread import *
import thread

# Create empty dictionary and list for clients trying to connect with the server
connected_users = {}
connectedusers = []

port = int(sys.argv[2])		# Store the value of port from command line in local variable

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print "socket created"
sock.bind(("",port))		# Bind the socket to all the hosts on machine and specified port
		
def client_new_thread(data, ip, port):
		try:
			# Check what the client is trying to send to the server
			addr = str(ip) + ":" + str(port)
			if data == 'list' or data == 'List':
				new_connected_users = []
				for k,v in connected_users.items():
                                        if k == addr:
                                                user_contacting = v	# retrieve the user who sent the 'list' command to the server
				for names in connectedusers:
					if names == user_contacting:
						continue
					else:
						new_connected_users.append(names)
				if len(new_connected_users) > 0:
					str1 = " ".join(map(str, new_connected_users))	# Create a string with names of other users signed in on the server
				else:
					str1 = "There are currently no users signed-in"
				sock.sendto(str1, (ip, port))
			elif "?" in data:
				username = data.split("?")[0]
				for k,v in connected_users.items():
                                        if v == username:
                                                addr = k
				sock.sendto(addr, (ip, port))
			elif len(data.split()) >= 3:
				print "You are trying to send a message"
				print data
				user = data.split(" ")[1]
				print user
				message = user + " " + ' '.join(w for w in data.split()[2:])
				for k,v in connected_users.items():
					if v == user:
						address = k
						print address
				addr_ip = address.split(":")[0]
				addr_port = address.split(":")[1]
				msg = message + "," + str(addr_ip) + ":" + str(addr_port)
				print msg
			# Here I am sending the ip-port of the user to the client		
				sock.sendto(msg, (ip, port))
			elif len(data.split()) == 1:
# Check if the user trying to send the sign in message is sending for the first time, if not store the new address from where same user is trying to login the server
				if data not in connectedusers:		# Check if the username is not in the connectedusers list 
					connected_users[addr] = data
					connectedusers.append(data)
				else:
					for k,v in connected_users.items():
						if v == data:
							old_addr = k
					connected_users[addr] = connected_users[old_addr] # Store the new key of the dictionary pointing to the new address and delete the old key
					del connected_users[old_addr]		
		except KeyboardInterrupt:
        		sock.close()
while True:
	data, (ip, port) = sock.recvfrom(1000)
	thread.start_new_thread(client_new_thread, (data, ip, port))	# For each new connection from the client, open a new thread
