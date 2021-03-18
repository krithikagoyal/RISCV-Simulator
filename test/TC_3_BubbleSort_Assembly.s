.data
	.word 10, 9, 8, 7, 6, 5, 4, 3, 2, 1 # Array, a

.text
	lui x10 65536 # Base address of array
    addi x11 x0 10 # Number of elements, n
    addi x12 x10 44 # Base address of sorted/new array
    
    addi x20 x0 0 # i
    add x21 x10 x0 # Copy of base address of original array
    add x22 x12 x0 # Copy of base address of sorted array
    
	loop: # To copy elements at new location
    	bge x20 x11 end_loop # If i >= 10
        lw x23 0(x21) # Load element at address given by x21
        sw x23 0(x22) # Store element at address given by x22
        addi x20 x20 1 # Increment i
        addi x21 x21 4 # Increment address of original array
        addi x22 x22 4 # Increment address of sorted array
        beq x0 x0 loop
		end_loop: # End loop
        
    add x20 x11 x0 # Copy of n
    addi x22 x0 1 # 1
    
	jal x1 bubble_sort # Call bubble sort
    beq x0 x0 exit # Exit program
    
    # Bubble sort procedure
    bubble_sort:
    	beq x20 x22 end # If n == 1
        
        addi sp sp -4 # Stack
        sw x1 0(sp) # Store return address
        
        addi x25 x0 0 # i
        addi x26 x20 -1 # n-1
        
        # One pass of bubble sort
        get_max:
        	bge x25 x26 end_get_max # If i >= n-1
            addi x27 x25 1 # i+1
            
            # Get offsets
            slli x27 x27 2 # (i+1)*4
            slli x28 x25 2 # i*4
            
            # Get addresses
            add x27 x27 x12 # Base address + offset
            add x28 x28 x12 # Base address + offset
            
            # Load values
            lw x29 0(x27) # a[i+1]
            lw x30 0(x28) # a[i]
            
            blt x30 x29 dont_swap
            sw x30 0(x27) # Swap
            sw x29 0(x28) # Swap
            
            dont_swap:
                addi x25 x25 1 # Increment i
                beq x0 x0 get_max # Reiterate
            
        end_get_max:
        
        addi x20 x20 -1 # Decrement n
        jal x1 bubble_sort # Recurse
        
        lw x1 0(sp) # Reload return address
        addi sp sp 4 # Restore stack
        
        end:
        	jalr x0 x1 0 # Return
    	
    
    # Exit program
    exit: