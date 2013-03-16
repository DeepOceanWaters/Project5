import socket
import re
 
COMP_PORT = 9878
REP_PORT  = 9879
MSG_LEN   = 8192

perfect_nums = []
cur_num = 0

def main():
	

def compute():
	# Create => bind => listen => accept the compute socket
	sock = create_sock_stream()
	bind_sock(sock, COMP_PORT)
	comp_sock, comp_addr = listen_and_accept(sock, 0)
	
	# Get timing information, generate and send an appropriate range
	time_str = sock.recv(MSG_LEN)
	time_num = int(time_str)
	max_num = get_max_num(time_num)
	max_range = str(max_num)
	sock.send(comp_range)
	
	# While compute does not signal that it's done, continue to recv
	while True:
		msg = sock.recv(MSG_LEN)
		if msg == 'done':
			return
		nums = parse_msg(msg)
		cur_num = int(nums[0])
		if nums[1] == "true":
			perfect_nums.append(cur_num)
		

## listen_and_accept:
##	takes a socket and the max number of backlog connects, then listens and
##	accepts.
## params:
##	sock: the socket to listen on
##	backlog: the number of backlog sockets allowed
## return: returns the sock.accept() return
##
def listen_and_accept(sock, backlog):
	sock.listen(backlog)
	return sock.accept()

## bind_sock:
## 	takes a socket and a port and binds the socket to the port.
## params:
##	sock: socket to bind
##	port: port to bind socket to
##
def bind_sock(sock, port):
	sock.bind((socke.gethostname(), port))

## create_sock:
## 	returns a newly created socket. Socket uses AF_INET and SOCK_STREAM
##
def create_sock_stream():
	return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

## kill_compute:
## 	takes a socket connected to a compute process, and sends a kill message
##	to the socket. The compute process should then terminate.
## params:
## 	sock: socket connected to the compute process
##
def kill_compute(sock):
	kill_msg = "shutdown"
	sock.send(kill_msg)

## parse_msg:
## 	takes a string, and parses it into an array of tab seperated values
## params:
## 	msg: the string to be parsed
##
def parse_msg(msg):
	tab_regex = re.compile(".*?\t+")
	return tab_regex.findall(msg)


if __name__ == "__main__":
	main()