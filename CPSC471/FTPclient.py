
# **********************************************************************
# FTPclient.py
# A simple FTP client.
# Authors: Jason Chandler, Justin Chandler, David Ngo, Christian Medina
# **********************************************************************

import socket
import signal
import os
import sys

def main():
	
	# Signal handler
	def signal_handler(signal, frame):
		
		# Check for connection socket and close it
		if 'connSocket' in locals():
			connSock.close()
		
		print " Interrupted"
		sys.exit(0)
	
	# Signal handler
	signal.signal(signal.SIGINT, signal_handler)
	
	# sys.argv contains the argument list
	# Checks for exactly two arguments
	if len(sys.argv) != 3:
		print "USAGE python " + sys.argv[0] + " <SERVER NAME>" + " <PORT NUMBER>" 
		print "1023 > PORT NUMBER < 65536"
		
	# Checks for valid port range and if the argument is a number
	elif int(sys.argv[2]) < 1023 or int(sys.argv[2]) > 65535 or not sys.argv[2].isdigit():
		print "USAGE python " + sys.argv[0] + " <SERVER NAME>" + " <PORT NUMBER>" 
		print "1023 > PORT NUMBER < 65536"
		
	else:

		# Server address
		serverAddr = sys.argv[1]

		# Server port
		serverPort = int(sys.argv[2])

		# Create a TCP socket
		connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# Connect to the server
		connSock.connect((serverAddr, serverPort))

		while True:
			
			size = ""
			
			# Get user input and parse into array
			cmd = raw_input("ftp> ").split()
			
			# Send buffer
			sndBuff = ""
			
			# GET command
			if cmd[0] == "get" and len(cmd) == 2:
				
				# Get size of receiver buffer and convert to string
				size = str(connSock.getsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF))
				
				# Pad string
				while len(size) < 10:
					size = "0" + size
				
				# Set command byte and add receiver buffer size
				sndBuff = chr(0) + size
				
				# Send data
				connSock.send(sndBuff)
					
				# ***************
				# CODE GOES HERE 
				# ***************
					
					
			# PUT command
			elif cmd[0] == "put" and len(cmd) == 2:
				
				# Get size of receiver buffer and convert to string
				size = str(connSock.getsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF))
				
				# Pad string
				while len(size) < 10:
					size = "0" + size
				
				# Set command byte and add receiver buffer size
				sndBuff = chr(1) + size
				
				# Send data
				connSock.send(sndBuff)
					
				# ***************
				# CODE GOES HERE 
				# ***************
					
					
			# LS command
			elif cmd[0] == "ls" and len(cmd) == 1:
				
				# Get size of receiver buffer and convert to string
				size = str(connSock.getsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF))
				
				# Pad string
				while len(size) < 10:
					size = "0" + size
				
				# Set command byte and add receiver buffer size
				sndBuff = chr(2) + size
				
				# Send data
				connSock.send(sndBuff)
					
				# ***************
				# CODE GOES HERE 
				# ***************
					
					
			# EXIT command
			elif cmd[0] == "exit" and len(cmd) == 1:
					
				# Set command byte
				sndBuff = chr(3)
				
				# Send data
				connSock.send(sndBuff)
					
				print("Exiting.")
				break
			
			# Invalid command
			else:
				print "\nInvalid command. Commands:"
				print "  get <FILE NAME>"
				print "  put <File NAME>"
				print "  ls"
				print "  exit\n"
		
		# Close the socket and the file
		connSock.close()
	
	sys.exit(0)

main()

