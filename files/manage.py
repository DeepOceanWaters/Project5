import socket
import re
 
COMP_PORT = 9878
REP_PORT  = 8753
MSG_LEN   = 4096
GIGA	  = 1000000

perfect_nums = []
cur_num = 0

def main():
	compute()



## compute:
## 	The function to call when starting the compute thread. Creates a socket
##	to listen to for a message from a client's compute. After creating the
##	socket, it should receive a message that details the timings of the
##	clients computer. Then it should determine the max num in the range of
##	numbers it will take the client about 15 seconds to compute.
##	Finally, enters an infinite loop and waits for either a kill signal
##	from the report thread, or for compute to return the 'done' message. 
##
def compute():
	# Create => bind => listen => accept the compute socket
	listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	listen_sock.bind((socket.gethostname(), COMP_PORT))
	print socket.gethostname()
	listen_sock.listen(1024)
	print "I ah aahham listennnniiinnnnnnnggggggggg"
	(comp_sock, comp_addr) = listen_sock.accept()
	print "I just accepted this fool"
	
	# Get timing information, generate and send an appropriate range
	msg = comp_sock.recv(MSG_LEN)
	print msg
	timings = parse_msg(msg)
	print timings
	max_num = gen_range(timings)
	max_range = str(max_num)
	comp_sock.send(comp_range)
	
	# While compute does not signal that it's done, continue to recv
	while True:
		msg = comp_sock.recv(MSG_LEN)
		if msg == 'done':
			return
		nums = parse_msg(msg)
		cur_num = int(nums[0])
		if nums[1] == "true":
			perfect_nums.append(cur_num)
			print msg



## gen_range:
##
##
def gen_range(timings):
	a = 1
	b = -1
	c = -2 * 15 * GIGA * long(timings[1]) / long(timings[0])
	max_num = (-b + math.sqrt(b * b - 4 * a * c)) / (2 * a)
	return int(max_num)


	
## report_t:
## 	The function to call when starting the report thread. Creates a socket
##	to listen to for a report call. Enters an infinite loop that calls
##	report_wait each time (i.e. it creates => listens => accepts on the
##	created socket, then takes the msg from the report call).
##
def report_t():
	# Create => bind => listen => accept the compute socket
	sock = create_sock_stream()
	bind_sock(sock, REP_PORT)
	
	while True:
		report_wait(sock)
	return


## report_wait:
##	Takes a socket and listens/accepts on that socket. Should receive a
##	message that is either "report" or "kill".
##	"report" => report the current state of things.
##	"kill"   => report the current state of things, then kill all processes
## params:
##	sock: the socket to listen/accept on
##
def report_wait(sock):
	rep_sock, rep_addr = listen_and_accept(sock, 0)
	msg = rep_sock.recv()
	
	if msg == 'report':
		report(rep_sock)
	elif msg == 'kill':
		report(rep_sock)
		kill_compute()
	
	# done



## report:
##	Takes a socket to send to. Creates a message and sends it to the report
##	socket. The message contains the current number and the perfect numbers
##	found.
##	message format: "CUR_NUM\tP_NUM[0]\tP_NUM[1]\t...\tP_NUM[n]"
##		example: "319\t6\t28" or "597\t6\t28\t496"
## params:
##	sock: the socket connected to the report calling the server for info
##
def report(sock):
	msg = ''
	msg = str(cur_num)
	p_nums = perfect_nums
	
	for p_num in p_nums:
		msg += '\t'
		msg += str(pnum)
	
	sock.send(msg)
	return
	


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
	sock.bind((socket.gethostname(), port))

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
	tab_regex = re.compile("[^\t]+\t*?")
	return tab_regex.findall(msg)


if __name__ == "__main__":
	main()