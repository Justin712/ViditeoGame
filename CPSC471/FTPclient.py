
# **********************************************************************
# FTPclient.py
# A simple FTP client.
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

def main():
	
	# Signal handler
	def signal_handler(signal, frame):
		
		# Check for connection socket and close it
		if 'connSocket' in locals():
			connSock.close()
		
		# Exit
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
	elif int(sys.argv[2]) < 1024 or int(sys.argv[2]) > 65535 or not sys.argv[2].isdigit():
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
			
			# Get user input and parse into array
			cmd = raw_input("ftp> ").split()
			
			# Send buffer
			sndBuff = ""
			
			# GET command
			# Check for "get" and appropriate arguments
			if cmd[0] == "get" and len(cmd) == 2:
				
				# Get size of receiver buffer and convert to string
				size = str(connSock.getsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF))
				
				# Pad string
				while len(size) < 10:
					size = "0" + size
				
				# Set command byte and add client receive buffer size
				sndBuff = chr(0) + size
				
				# Send data
				connSock.send(sndBuff)
					
				# ***************
				# CODE GOES HERE 
				# ***************
					
					
			# PUT command
			# Check for "put" and appropriate arguments
			elif cmd[0] == "put" and len(cmd) == 2:
				
				# Get size of receiver buffer and convert to string
				size = str(connSock.getsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF))
				
				# Pad string
				while len(size) < 10:
					size = "0" + size
				
				# Set command byte and add client receive buffer size
				sndBuff = chr(1) + size
				
				# Send data
				connSock.send(sndBuff)
					
				# ***************
				# CODE GOES HERE 
				# ***************
					
					
			# LS command
			# Check for "ls" and appropriate arguments
			elif cmd[0] == "ls" and len(cmd) == 1:
				
				# Get size of receiver buffer and convert to string
				size = str(connSock.getsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF))
				
				# Pad string
				while len(size) < 10:
					size = "0" + size
				
				# Set command byte and add client receiver buffer size
				sndBuff = chr(2) + size
				
				# Send data
				connSock.send(sndBuff)
					
				# ***************
				# CODE GOES HERE 
				# ***************
					
					
			# EXIT command
			# Check for "exit" and appropriate arguments
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
		
		# Close the socket
		connSock.close()
	
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

