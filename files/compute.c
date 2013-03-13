/* Compute
 *
 *
 */

// includes...
#include <stdio.h>
#include <stdlib.h>

// defs...

// 
int is_perfect(int num);
int is_perfect_helper(int cur, int num);

int main (int argc, const char * argv[])
{
	int num;
	num = atoi(argv[1]);
	if(is_perfect(num))
		printf("%d is perfect\n", num);
	else
		printf("%d is not perfect\n", num);
	
	return 0;
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
