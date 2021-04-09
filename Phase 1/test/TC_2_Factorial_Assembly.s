.data
	.word 10 # n in n!

.text
    lui x28 65536 # x28 = 0x10000000 i.e. address of n
    lw x10 0(x28) # Load n in x10
    jal x1 fact # Call factorial
    sw x10 4(x28)
    beq x0 x0 exit # Exit program

    # Factorial procedure
    fact:
        addi sp sp -8 # Stack
        sw x1 4(sp) # Store return address
        sw x10 0(sp) # Store current value
        addi x5 x10 -1 # Get x - 1 for x input in the procedure
        addi x7 x0 1 # Get 1
        bge x5 x7 L1 # If x - 1 >= 1, go to L1
        addi x10 x0 1 # 0! = 1
        addi sp sp 8 # Restore stack
        jalr x0 x1 0 # Return
        L1:
            addi x10 x10 -1 # x = x - 1
            jal x1 fact # Call factorial
            addi x6 x10 0 # Get result
            lw x10 0(sp) # Load initial value
            lw x1 4(sp) # Load return address
            addi sp sp 8 # Restore stack
            mul x10 x10 x6 # Get answer
            jalr x0 x1 0 # Return

    # Exit program
    exit:
