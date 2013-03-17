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

// defs...
#define TEST_MAX 5000
#define MEGA	 1000000

// functions...
void get_timings(char *timings);
long long get_ops();
double get_timed_total();
int is_perfect(int num);
int is_perfect_helper(int cur, int num);




int main (int argc, const char * argv[])
{
	int num;
	char *timings;
	
	timings = (char *) malloc(100 * sizeof(char));
	get_timings(timings);
	printf("timings: %s\n", timings);
	
	return 0;
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