
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
	numBytes = int(numBytes)
	# The buffer
	recvBuff = ""
	
	# The temporary buffer
	tmpBuff = ""
	
	# Keep receiving till all is received
	while len(recvBuff) < (numBytes):
		
		# Attempt to receive bytes
		tmpBuff =  sock.recv(numBytes)
		
		# The other side has closed the socket
		if not tmpBuff:
			break
		
		# Add the received bytes to the buffer
		recvBuff += tmpBuff
		
	return str(recvBuff)

def main():
	
	# Signal handler
	def signal_handler(signal, frame):
		
		# Check for welcome socket and close it
		if 'welcomeSock' in locals():
			welcomeSock.close()
		
		# Check for client socket and close it
		if 'clientSock' in locals():
			clientSock.close()

		if 'servData' in locals():
			servData.close()

		if 'clientData' in locals():
                        clientData.close()
		
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
                        
			        # Size of receive buffer as 10-digit string
                                servSize = ""
                                servSize = str(clientSock.getsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF))
                                while (len(servSize) < 19):
                                        servSize = "0" + servSize

                        
				# GET command
				if cmd == 0:
                                        # Size of client receive buffer
                                        bufSize = ""
                                        bufSize = recvAll(clientSock, 19)
                                        bufSize = int(bufSize)
                                        
                                        print "Client buffer size = ", bufSize, " bytes"
                                        
                                        # Receive name of file to send
                                        fileNLength = recvAll(clientSock, 2)
                                        fileN = str(recvAll(clientSock, fileNLength))
                                        print "Request for file ", fileN, " received."
                                        
                                        # Open requested file for reading and print its size
                                        try:
                                                reqFile = open(fileN, 'rb+')
                                                print fileN, " opened for reading."
                                        
                                        # Handles IO errors.
                                        except IOError as e:
                                                print "IO ERROR:\t *** %s ***" % print_error(e.errno)
                                                break
                                        
                                        fileSize = (os.fstat(reqFile.fileno()).st_size)
                                        print "Detected file size is ", fileSize, " bytes"
                                        
                                        if fileSize <= 0:
                                                print "Error: cannot send 0 byte file."
                                                break
                                        
                                        # Construct data socket, bind it to an ephemeral port,
                                        # then open for connections
                                        servData = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                        servData.bind(('',0))
                                        newPort = str(servData.getsockname()[1])
                                        newPortLength = len(str(newPort))
                                        newPortLength = str(newPortLength)
                                        
                                        #Send client the new data transfer port
                                        clientSock.send(newPortLength)
                                        clientSock.send(newPort)
                                        servData.listen(1)
                                        
                                        print "Ephemeral port number for GET: ", servData.getsockname()[1]
                                        clientData, addr2 = servData.accept()
                                        
                                        # Commence Transfer
                                        numBytes = str(fileSize)
                                        while len(numBytes) < 19:
                                                numBytes = "0" + numBytes
                                        clientData.send(numBytes)
                                        while True:
                                                packet = reqFile.read(bufSize)
                                                if not packet:
                                                        break
                                                clientData.sendall(packet)
                                                
					print "SUCCESS: GET"
					print '\n', "Awaiting further commands..."
					reqFile.close()
					servData.close()
					                
				# PUT command
				elif cmd == 1:
                                        
				        # Send max buffer size
                                        clientSock.sendall(servSize)
                                        
                                        # Receive name of file to be sent
                                        fileNLength = recvAll(clientSock, 2)
                                        fileN = str(recvAll(clientSock, fileNLength))
                                        print "Incoming PUT request for file ", fileN, " received."
                                        
                                        # Construct data socket, bind it to an ephemeral port,
                                        # then open for connections
                                        servData = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                        servData.bind(('',0))
                                        newPort = str(servData.getsockname()[1])
                                        newPortLength = len(str(newPort))
                                        newPortLength = str(newPortLength)
                                        
                                        #Send client the new data transfer port
                                        clientSock.send(newPortLength)
                                        clientSock.send(newPort)
                                        servData.listen(1)
                                        
                                        print "Ephemeral port number for GET: ", servData.getsockname()[1]
                                        clientData, addr2 = servData.accept()
                                        
                                        # Commence Transfer
                                        numBytes = recvAll(clientData, 19)
                                        print "File requested is ", int(numBytes), " bytes"
                                        fileN = str(fileN) + '.PUT'
                                        transferFile = open(fileN, 'wb+')
                                        dataBuff = ""
                                        receivedBytes = 0
                                        
                                        while (receivedBytes < int(numBytes)):
                                                dataBuff += recvAll(clientData, int(numBytes))
                                                transferFile.write(dataBuff)
                                                receivedBytes += len(dataBuff)
                                                print receivedBytes, "/", int(numBytes), "bytes received."
                                        transferFile.close()
                                        print "SUCCESS: PUT"
                                        servData.close()

                                # LS Command
				elif cmd == 2:
                                        # Size of client receive buffer
                                        bufSize = ""
                                        bufSize = recvAll(clientSock, 19)
                                        bufSize = int(bufSize)
                                        
                                        print "Client buffer size = ", bufSize, " bytes"
                                        
                                        print "Request for LS received."

                                        os.system('ls > LS_Record.txt')
                                        
                                        # Open requested file for reading and print its size
                                        reqFile = open('LS_Record.txt', 'rb+')
                                        print "LS_Record.txt opened for reading."
                                        
                                        fileSize = (os.fstat(reqFile.fileno()).st_size)
                                        print "Detected file size is ", fileSize, " bytes"
                                        
                                        if fileSize <= 0:
                                                print "Error: cannot send 0 byte file."
                                                break
                                        
                                        # Construct data socket, bind it to an ephemeral port,
                                        # then open for connections
                                        servData = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                        servData.bind(('',0))
                                        newPort = str(servData.getsockname()[1])
                                        newPortLength = len(newPort)
                                        newPortLength = str(newPortLength)
                                        
                                        #Send client the new data transfer port
                                        clientSock.sendall(newPortLength)
                                        clientSock.sendall(newPort)
                                        servData.listen(1)
                                        
                                        print "Ephemeral port number for LS: ", int(newPort)
                                        clientData, addr2 = servData.accept()

                                        # Send file name length, then file name
                                        #sndBuff = str(len('LS_Record'))
                                        #clientSock.sendall(sndBuff)
                                        #sndBuff = 'LS_Record'
                                        #clientSock.sendall(sndBuff)

                                        # Commence Transfer
                                        numBytes = str(fileSize)
                                        while len(numBytes) < 19:
                                                numBytes = "0" + numBytes
                                        clientData.send(numBytes)
                                        while True:
                                                packet = reqFile.read(bufSize)
                                                if not packet:
                                                        break
                                                clientData.sendall(packet)
                                                
					print "SUCCESS: LS"
					print '\n', "Awaiting further commands..."
					reqFile.close()
					clientData.close()
                                        servData.close()
					                        
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
                        
			conn = raw_input("Continue waiting for connections? (y/n)")
			if conn != 'y':
                                break
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

