import math
import re
import socket
import signal
import thread
 
SERV_PORT = 9878
REP_PORT  = 9880
MSG_LEN   = 4096
GIGA	  = 1000000

perfect_nums = []
cur_num = 0


def isodd(x): x & 1


def main():
	thread.start_new_thread(listen_rep, ("Report-Thread", 2))
	compute()
	return




def listen_rep(thread_name, nums):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((socket.gethostname(), REP_PORT))
	sock.listen(1024)
	r_sock, r_addr = sock.accept()
	r_regex = re.compile("kill");
	msg = r_sock.recv(MSG_LEN)
	print thread_name + ": " + msg
	r_sock.send("information\t")
	if len(r_regex.findall(msg)) > 0:
		print "something" # signal and kill
	return


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
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((socket.gethostname(), SERV_PORT))
	sock.listen(1024)
	comp_sock, comp_addr = sock.accept()
	
	# Get timing information, generate and send an appropriate range
	msg = comp_sock.recv(MSG_LEN)
	timings = parse_msg(msg)
	max_num = gen_range(timings)
	max_range = str(max_num)
	comp_sock.send(max_range)
	
	cnt = 0
	comp_bool = True
	has_remainder = False
	msg = ''
	comp_msg = 'init'
	cmp_regex = re.compile("done\t");
	# While compute does not signal that it's done, continue to recv
	while True:
		if comp_bool:
			comp_msg = comp_sock.recv(MSG_LEN)
			if len(cmp_regex.findall(comp_msg)) > 0:
				comp_bool = False
		else:
			break
		msg = msg + comp_msg
		nums, msg = parse_results(msg)
		for num in range(0, len(nums) - 1, 2):
			cur_num = nums[num]
			if nums[num + 1] == 'true':
				perfect_nums.append(cur_num)
				print "[" + max_range + "] Perfect: " + cur_num
	
	print "Perfect Nums"
	for item in perfect_nums:
		print item
	print "I guess I am done."



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


## parse_results
##
##
def parse_results(msg):
	tab_regex = re.compile("[^(\t\x00)]+\t*")
	nums = tab_regex.findall(msg)
	remainder = ''
	if isodd(len(nums)):
		remainder += nums[-1]
		nums = nums[:-1]
	elif nums[-1][-1] != "\t":
		remainder += nums[-2]
		remainder += nums[-1]
		nums = nums[:-2]
	for num in range(0, len(nums)):
		nums[num] = nums[num][:-1]
	return nums, remainder


## parse_msg:
## 	takes a string, and parses it into an array of tab seperated values
## params:
## 	msg: the string to be parsed
##
def parse_msg(msg):
	tab_regex = re.compile("[^(\t\x00)]+\t*?")
	return tab_regex.findall(msg)


if __name__ == "__main__":
	main()
