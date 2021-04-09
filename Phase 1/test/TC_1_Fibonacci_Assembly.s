.data
	.word 20, 0, 1 # n, seed values(i.e. n1, n2)

.text
	lui x10 65536 # Address of n
    addi x11 x10 12 # Address of n3
    
    lw x12 0(x10) # Load n
    addi x12 x12 -2 # n = n - 2
    lw x20 4(x10) # Load n1
    lw x21 8(x10) # Load n2
	
    jal x1 fib # Call fib
    beq x0 x0 exit # Exit program
    
    # Fibonacci procedure
    fib:
    	beq x12 x0 end # If n == 0
        addi sp sp -4 # Stack
        sw x1 0(sp) # Store return address
        add x13 x20 x21 # n(i) = n(i-1) + n(i-2)
        sw x13 0(x11) # Store ni
        addi x11 x11 4 # Increment address
        add x20 x21 x0 # Reset last 2 numbers in the series
        add x21 x13 x0 # Reset last 2 numbers in the series
        addi x12 x12 -1 # Decrement n
        jal x1 fib # Call fib
        lw x1 0(sp) # Reload address
        addi sp sp 4 # Restore stack
        end:
        	jalr x0 x1 0 # Return
    
    # Exit program
    exit: