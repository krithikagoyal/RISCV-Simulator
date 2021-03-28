# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#convert machine code to proper hexa.
def getHex(s):
    s=s[2::]
    size =len(s);
    if size == 1:
        s = "0000000" + s
    if size == 2:
        s = "000000" + s
    if size == 3:
        s = "00000" + s
    if size == 4:
        s = "0000" + s
    if size == 5:
        s = "000" + s
    if size == 6:
        s = "00" + s
    if size == 7:
        s = "0" + s
    return s



#input is hexa
def getBin(s):
    hexcodes={
        '0':"0000",
        '1':"0001",
        '2':"0010",
        '3':"0011",
        '4':"0100",
        '5':"0101",
        '6':"0110",
        '7':"0111",
        '8':"1000",
        '9':"1001",
        'A':"1010",'a':"1010",
        'B':"1011",'b':"1011",
        'C':"1100",'c':"1100",
        'D':"1101",'d':"1101",
        'E':"1110",'e':"1110",
        'F':"1111",'f':"1111"
        }
    size=len(s);
    converted=""
    i=0
    while i<size:
        converted=converted+hexcodes[s[i]]
        i=i+1
        
    return converted ;   
        
    
            
    

hexa=input()
hexa=hexa.split()
hexa=hexa[1]
#now we have hex in the form 0xxxxxxxx
hexa=getHex(hexa);
#Now We have main machine code in hexa.
hexa=getBin(hexa);
#Now we have binary code in hexa
#Now we need to do decoding part



    
    