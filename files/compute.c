/* Compute
 *
 *
 */

// includes...
#include <stdio.h>
#include <stdlib.h>

// defs...

// 
void is_perfect_range(int num);
int is_perfect(int num);
int is_perfect_helper(int cur, int num);

int main (int argc, const char * argv[])
{
	int num;
	num = atoi(argv[1]);
	is_perfect_range(num);
	
	return 0;
}


void is_perfect_range(int num)
{
	for(int i = 2; i <= num; i++)
		if(is_perfect(i))
			printf("%d is perfect\n", i);
}


/* is_pefect
 * Description:
 *	Checks if a given number is perfect.
 * Params:
 *	num = number to check
 */
int is_perfect(int num)
{
	return (num == is_perfect_helper(1, num));
}

int is_perfect_helper(int cur, int num)
{
	if(cur == num)
		return 0;
	if(num % cur == 0)
		return cur + is_perfect_helper(cur + 1, num);
	return is_perfect_helper(cur + 1, num);
}
