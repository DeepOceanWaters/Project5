import socket
import getopt
import sys

SERV_PORT = 9880
MSG_LEN   = 4096


def main():
        try:
        	opts, args = getopt.getopt(sys.argv[1:], ":k", ["kill"])
        except getopt.GetoptError as err:
           	# print help information and exit:
		print str(err)
		usage()
        	sys.exit(2)
	if len(args) < 1:
		print "Enter an ip address"
		return
	ip_addr = args[0]
	
	# Create => bind => listen => accept the compute socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((ip_addr, SERV_PORT))
	
	if len(opts) > 0:
		if opts[0] == '-k':
			send_kill(sock)
			return
	get_info(sock)
	return


def get_info(sock):
	msg_manager(sock, "report\t")
	return

def send_kill(sock):
	msg_manager(sock, "kill\t")
	return

def msg_manager(sock, msg):
	sock.send(msg)
	new_msg = sock.recv(MSG_LEN)
	print new_msg
	return


if __name__ == "__main__":
	main()
