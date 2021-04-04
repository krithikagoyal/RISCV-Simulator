Description:
1. Fibonacci - Generates Fibonacci series. The first two seed values and the number of elements required is pre-loaded in the memory. The series is stored in the memory after the input data.
2. Factorial - Generates n!. The value of n is pre-loaded in the memory. The value of n! is stored at 0x10000004 i.e. after the pre-loaded data.
3. Bubble sort - Sorts the given array in ascending order. The array is pre-loaded in the memory. The output is stored in the memory one word after the pre-loaded data.

Note:
1. Above 3 test cases are implemented recursively.
2. The test cases are mostly based on the tasks given in the labs.
3. Exit instruction is 0x401010BB(i.e. subw x1, x1, x1).
