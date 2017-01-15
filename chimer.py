#!/usr/bin/env python2.7  
# Button action script by Phil Leinster
# Socket server in python using select function
# taken from http://www.binarytides.com/python-socket-server-code-example/
# V1.0 29.05.2016

import select, subprocess, threading, socket, signal
from settings import PORT

class GracefulKiller:
	kill_now = False
	def __init__(self):
		signal.signal(signal.SIGINT, self.exit_gracefully)
		signal.signal(signal.SIGTERM, self.exit_gracefully)

	def exit_gracefully(self,signum, frame):
		print "Recieved " + SIGNNAME[signum] + "."
		self.kill_now = True
		raise SystemExit

def chime():
	subprocess.call(["sudo", "amixer", "set", "PCM", "--", "65000"])
	subprocess.call(["sudo", "aplay", "/usr/local/bin/chimerd/doorbell.wav"])
	subprocess.call(["sudo", "amixer", "set", "PCM", "--", "0"])

SIGNNAME = dict((getattr(signal, n), n) \
for n in dir(signal) if n.startswith('SIG') and '_' not in n )

if __name__ == "__main__":
	killer = GracefulKiller()
	CONNECTION_LIST = []    # list of socket clients
	RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
	 
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# this has no effect, why ?
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind(("0.0.0.0", PORT))
	server_socket.listen(10)
	
	# Add server socket to the list of readable connections
	CONNECTION_LIST.append(server_socket)
	
	print "Chat server started on port " + str(PORT)
	
	run = 1
	while run == 1:
		# Get the list sockets which are ready to be read through select
		try:
			read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
		except:
			if killer.kill_now:
				break
		
		for sock in read_sockets:
			 
			#New connection
			if sock == server_socket:
				# Handle the case in which there is a new connection recieved through server_socket
				sockfd, addr = server_socket.accept()
				CONNECTION_LIST.append(sockfd)
				print "Client (%s, %s) connected" % addr
				sockfd.send('Command> ')
			#Some incoming message from a client
			else:
				# Data recieved from client, process it
				try:
					#In Windows, sometimes when a TCP program closes abruptly,
					# a "Connection reset by peer" exception will be thrown
					data = sock.recv(RECV_BUFFER)
					# echo back the client message
					if data:
						#print "Rx: " + data
						data = data.rstrip('\r\n')
						if ( data.lower() == 'q' or data.lower() == 'quit'):
							sock.send('\nbye!\n\n')
							sock.close()
							CONNECTION_LIST.remove(sock)
							continue
						elif ( data.lower() == 'shutdown'):
							for socks in read_sockets:
								socks.send('\nServer is shutting down... bye!\n\n')
							run = 0
						elif ( data.lower() == 'chime'):
							sock.send('Starting chimer... ')
							t1 = threading.Thread(target=chime)
							t1.start()
							sock.send(' done.')
							sock.send('\nCommand> ')
						elif ( data.startswith("irsend ")):
							#print "attempting irsend"
							try:
								stout = subprocess.Popen(data, stdout=subprocess.PIPE, shell=True)
							except Exception as e:
								print e
							print stout
						else:
							sock.send('bad command: ' + data)
							sock.send('\nCommand> ')
				except:
					# client disconnected, so remove from socket list
					print "Client (%s, %s) is offline" % addr
					sock.close()
					CONNECTION_LIST.remove(sock)
					if killer.kill_now:
						break
					continue
	print "Server is shutting down."
	server_socket.close()




