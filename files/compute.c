/* Compute                                                                    *
 * ========================================================================== *
 * Author: Colin Bradford                                                     *
 * Date: 3/17/2013                                                            *
 *                                                                            *
 * CS 311: Project 5                                                          *
 *                                                                            *
 */


// includes...
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/time.h>
#include <time.h>
#include <math.h>
#include <string.h>
#include <sys/socket.h>	/* basic socket definitions */

// defs...
#define TEST_MAX  5000
#define MEGA	  1000000
#define SERV_PORT 9878
#define MAXLINE   4096

// functions...


void child_sig(int signum);
void parent_sig(int signum);
void handle_sigs(int signum, void (*sa_handler)(int));
void signal_process(int sockfd);
void numbers_process(int sockfd, int max_num);
struct sockaddr_in creat_servaddr(char *ip_addr);
void is_perfect_loop(int max_num, int sockfd);
void get_timings(char *timings);
long long get_ops();
double get_timed_total();
int is_perfect(int num);
int is_perfect_helper(int cur, int num);




int main (int argc, const char * argv[])
{
	struct sockaddr_in servaddr;
	char sendline[MAXLINE];
	int max_num;
	int sockfd;
	
	
	if(argc < 2) {
		printf("Please enter an ip address\n");
		exit(EXIT_FAILURE);
	}
	
	// create socket, create servaddr, & connect to server
	sockfd = socket(AF_INET, SOCK_STREAM, 0);
	servaddr = creat_servaddr(argv[1]);
	connect(sockfd, (struct sockaddr *) &servaddr.sin_addr);
	
	// generate & send timings
	get_timings(sendline);
	write(sockfd, sendline, strlen(sendline) + 1);
	
	// wait to recv max_num from server
	max_num = get_max_num(sockfd);
	
	// create signal process
	switch(fork()) {
	case -1:
		perror("Fork");
		exit(EXIT_FAILURE);
	case  0:
		signal_process(sockfd);
		_exit(EXIT_FAILURE);
	default:
		numbers_process(sockfd, max_num);
		break;
	}
	
	return 0;
}



/* parent_sig
 *
 */
void *parent_sig(int signum)
{
	// do stuff
	exit(EXIT_SUCCESS);
}



/* child_sig
 *
 */
void *child_sig(int signum)
{
	// do stuff
	_exit(EXIT_SUCCESS);
}



/* handle_sigs
 * Might need more work
 */
void handle_sigs(int signum, void (*sa_handler)(int))
{
	struct sigaction s;
	struct sigaction t;
	
	s.sa_flags = 0;
	s.sa_handler = sa_handler;
	sigemptyset(&s.sa_mask);
	sigaction(signum, &s, &t);
	
	return;
}



/* signal_process
 * NEED TO FINISH || Can still try out connection when no signal is passed tho
 */
void signal_process(int sockfd)
{
	char recvline[MAXLINE];
	
	// handle signals
	handle_sigs(SIGINT,  (void *) child_sig);
	handle_sigs(SIGHUP,  (void *) child_sig);
	handle_sigs(SIGQUIT, (void *) child_sig);
	
	/* 30x sleep 2 seconds then read; print what is read; finally _exit() */
	/* allow to test without going into an infinite loop */
	for(int i = 0; i < 30; i++) {
		sleep(2);
		bzero(recvline, MAXLINE);
		if(read(sockfd, recvline, MAXLINE) == 0){
			perror("signal_process reading socket");
			_exit(EXIT_FAILURE);
		}
		printf("Child recieved: %s\n", recvline);
	}
	_exit(EXIT_SUCCESS);
	/* Remove this when we want to test the signal process for real */
	/* Otherwise, don't want to go into an infinite loop by accident */
	
	// go into infinite loop, waiting for a kill signal/message
	for(;;) {
		bzero(recvline, MAXLINE);
		if(read(sockfd, recvline, MAXLINE) == 0){
			perror("signal_process reading socket");
			_exit(EXIT_FAILURE);
		}
		// if recvline == "kill", kill the program
		// 	kill: Signal other process. Cleanup.
		// else ignore
	}
	
	_exit(EXIT_SUCCESS);
}



/* numbers_process
 *
 */
void numbers_process(int sockfd, int max_num)
{
	char sendline[MAXLINE];
	
	// handle signals
	handle_sigs(SIGINT,  (void *) parent_sig);
	handle_sigs(SIGHUP,  (void *) parent_sig);
	handle_sigs(SIGQUIT, (void *) parent_sig);
	
	// loop through range to check for perfect numbers
	for(int i = 2; i <= max_num; i++) {
		memcpy(sendline, '', MAXLINE);
		if(is_perfect(i)) {
			sprintf(sendline, "%d\ttrue", i);
		}
		else {
			sprintf(sendline, "%d\tfalse", i);
		}
		write(sockfd, sendline, strlen(sendline) + 1);
	}
	memcpy(sendline, 'done', MAXLINE);
	write(sockfd, sendline, strlen(sendline) + 1);
	
	// done with socket, closing it
	close(sockfd);
	
	return;
}



/* get_max_num
 *
 */
int get_max_num(int sockfd)
{
	char recvline[MAXLINE];
	int max_num;
	
	// wait to recv max_num from server
	bzero(recvline, MAXLINE);
	if(read(sockfd, recvline, MAXLINE) == 0){
		perror("Reading from socket");
		exit(EXIT_FAILURE);
	}
	
	/* strcmp returns 0 if strings match */
	if(!strcmp(recvline, "kill")) {
		// kill
	}
	
	// convert max_num from server to a num
	// Note: might need to regex this because python sends weird chars???
	max_num = atoi(recvline);
	
	return max_num;
}



/* creat_servaddr
 *
 */
struct sockaddr_in creat_servaddr(char *ip_addr)
{
	struct sockaddr_in servaddr;
	
	// create servaddr
	bzero(&servaddr, sizeof(servaddr));
	servaddr.sin_family = AF_INET;
	servaddr.sin_port = htons(SERV_PORT);
	inet_pton(AF_INET, ip_addr, &servaddr.sin_addr);
	
	return servaddr;
}



/* get_timings
 *
 */
void get_timings(char *timings)
{
	long long num_ops;	/* number of operations (roughly) */
	double micro_avg;	/* the average of multiple micro samples*/
	
	
	num_ops = get_ops();
	micro_avg = 0;
	
	for(int j = 0; j < 20; j++)
		micro_avg += get_timed_total() / 20;
	
	// Print total time (micro) and num of operations to the timings buf
	sprintf(timings, "%lld\t%lld", (long long) micro_avg, num_ops);
	
	// !! REMEMBER !!
	// Still need to calculated the new_max in python/server part
	
	return;
}



/* get_ops
 *
 */
long long get_ops()
{
	long long num_ops;
	
	num_ops = (TEST_MAX + 1) * TEST_MAX * 30 / 59;
	
	for(int i = 2; i <= TEST_MAX / 2; i++)
		num_ops += (TEST_MAX - i) / i * 61 / 59;
	
	return num_ops;
}



/* get_timed_total
 *
 */
double get_timed_total()
{
	struct timeval start;	/* the time before performing the operations */
	struct timeval end;	/* the time after performing the operations */
	double micro_total;
	char buf[50];
	
	gettimeofday(&start, NULL);
	for(int i = 2; i <= TEST_MAX; i++) {
		memcpy(buf, "", 50);
		if(is_perfect(i)) {
			sprintf(buf, "%d\ttrue", i);
		}
		else {
			sprintf(buf, "%d\tfalse", i);
		}
		printf(""); /* simulate sending to socket */
	}
	gettimeofday(&end, NULL);
	
	// Calculate the time it took in micro seconds
	micro_total  = end.tv_usec;
	micro_total += end.tv_sec * MEGA;
	micro_total -= start.tv_usec;
	micro_total -= start.tv_sec * MEGA;
	return micro_total;
}




/* is_perfect
 * Description:
 *	Checks if a given number is perfect.
 * Params:
 *	num = number to check
 * Return:
 *	True if the give number (num) is a perfect number, otherwise it 
 *	returns false.
 */
int is_perfect(int num)
{
	return (num == is_perfect_helper(1, num));
}



/* is_perfect_helper
 * 
 */
int is_perfect_helper(int cur, int num)
{
	if(cur == num)
		return 0;
	if(num % cur == 0)
		return cur + is_perfect_helper(cur + 1, num);
	return is_perfect_helper(cur + 1, num);
}





/* ============================= END OF FILE =============================== */