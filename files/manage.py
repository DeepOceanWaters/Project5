import socket
import re

def main():
	

## kill_compute:
## 	takes a socket connected to a compute process, and sends a kill message
##	to the socket. The compute process should then terminate.
## params:
## 	sock: socket connected to the compute process
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