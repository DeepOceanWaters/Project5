import socket
import re

def main():
	

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