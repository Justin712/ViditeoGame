
# **********************************************************************
# FTPserver.py
# A simple FTP server.
# Authors: Jason Chandler, Justin Chandler, David Ngo, Christian Medina
# **********************************************************************

import errno
import os
import signal
import socket
import sys

# Prints error information
def print_error(errnum):
	
	# Returns error code and error message
	return "%s: %s" % (errno.errorcode[errnum], os.strerror(errnum))

# ************************************************
# Receives the specified number of bytes
# from the specified socket
# @param sock - the socket from which to receive
# @param numBytes - the number of bytes to receive
# @return - the bytes received
# *************************************************
def recvAll(sock, numBytes):
	
	# The buffer
	recvBuff = ""
	
	# The temporary buffer
	tmpBuff = ""
	
	# Keep receiving till all is received
	while len(recvBuff) < numBytes:
		
		# Attempt to receive bytes
		tmpBuff =  sock.recv(numBytes)
		
		# The other side has closed the socket
		if not tmpBuff:
			break
		
		# Add the received bytes to the buffer
		recvBuff += tmpBuff
		
	return recvBuff

def main():
	
	# Signal handler
	def signal_handler(signal, frame):
		
		# Check for welcome socket and close it
		if 'welcomeSock' in locals():
			welcomeSock.close()
		
		# Check for client socket and close it
		if 'clientSock' in locals():
			clientSock.close()
		
		# Exit
		print " Interrupted"
		sys.exit(0)
	
	# Signal handler
	signal.signal(signal.SIGINT, signal_handler)
	
	# sys.argv contains the argument list
	# Checks for exactly one argument
	if len(sys.argv) != 2:
		print "USAGE python " + sys.argv[0] + " <PORT NUMBER>"
		print "1023 > PORT NUMBER < 65536"

	# Checks for valid port range and if the argument is a number
	elif int(sys.argv[1]) < 1024 or int(sys.argv[1]) > 65535 or not sys.argv[1].isdigit():
		print "USAGE python " + sys.argv[0] + " <PORT NUMBER>"
		print "1023 > PORT NUMBER < 65536"
	
	else:
		
		# The port on which to listen
		listenPort = int(sys.argv[1])
		
		# Create a welcome socket. 
		welcomeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		# Bind the socket to the port
		welcomeSock.bind(('', listenPort))
		
		# Start listening on the socket
		welcomeSock.listen(1)
		
		# Accept connections forever
		while True:
			
			print "Waiting for connections..."
			
			# Accept connections
			clientSock, addr = welcomeSock.accept()
			
			print "Accepted connection from client: ", addr
			print "\n"
			
			while True:
				
				# The buffer to all data received from the the client.
				command = ""
				
				# The temporary buffer to store the received data.
				recvBuff = ""
				
				# Get the command byte
				command = recvAll(clientSock, 1)
				
				# Check command byte
				if not command:
					break
				
				# ord() to convert the ascii character into a decimal
				cmd = ord(command)
				
				# Size of receive buffer
				# print clientSock.getsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF)
				
				# GET command
				if cmd == 0:
					print "SUCCESS: GET"
					
					# Get max size of client receive buffer
					clientBuff = recvAll(clientSock, 10)
					
					# ***************
					# CODE GOES HERE 
					# ***************
					
					
				# PUT command
				elif cmd == 1:
					print "SUCCESS: PUT"
					
					# Get max size of client receive buffer
					clientBuff = recvAll(clientSock, 10)
					
					# ***************
					# CODE GOES HERE 
					# ***************
					
					
				# LS command
				elif cmd == 2:
					print "SUCCESS: LS"
					
					# Get max size of client receive buffer
					clientBuff = recvAll(clientSock, 10)
					
					# ***************
					# CODE GOES HERE 
					# ***************
					
					
				# EXIT command
				elif cmd == 3:
					print "SUCCESS: EXIT"
					break
					
				# Invalid command
				else:
					print"FAILURE: ", cmd
					
			print "\n\nClosing connection to client: ", addr
			
			# Close our side
			clientSock.close()
	
	# Exit
	sys.exit(0)

# Run main
try:
	main()
	
# Catch socket errors and print
except socket.error as e:
	print "SOCKET ERROR:\t *** %s ***" % print_error(e.errno)
	
# Catch address errors and print
except socket.herror as e:
	print "ADDRESS ERROR:\t *** %s ***" % print_error(e.errno)
	
# Catch additional address errors and print
except socket.gaierror as e:
	print "ADDRESS ERROR:\t *** %s ***" % print_error(e.errno)
	
# Catch timeouts and print
except socket.timeout as e:
	print "TIMEOUT ERROR:\t *** %s ***" % print_error(e.errno)

