'''
A Virtual Computer based on the 6502 Microprocessor
along with VC22 Versatile Interface Adapter and Generic RAM & ROM.
Written by Shreyan Dey.
Copyright(c) 2020 Shreyan Dey.
All Rights Reserved.
System v9.0
Last compiled on 4 August 2020.

CPU: VC02 v7.5
Architecture: VC02MIS
inst_regructions: 26
Execution cores: 1
Address width: 16 Bit
Data width: 8 Bit
Data format: Big Endian
Clock speed: 1MHz
Max memory : 64 K
Reset Vectors: 0xFFFC(High Byte),0XFFFD(Low Byte)
Page size: 256 B
Total Pages: 256(65536 Bytes)
Zero Page: 0x0000 to 0x00FF(Page 0)
Stack: 0x0100 to 0x01FF(Page 1)

RAM Module: v3.0
ROM Module: v3.0
VC22: v1.5
'''


import time
import sys
import numpy as np
import math

#--------system memory setup--------
sram=list() #RAM
prom=list() #ROM
def init_ram(size):
    for i in range(0,size):
        sram.append(0)
def init_rom():
    try:
        f=open("VC28C.rom","rb")
        temp=list(f.read())
        f.close()
        for i in range(len(temp)):
            prom.append(temp[i])
    except:
        print("ROM not found ERROR.")
        sys.exit()
#-------------------------
        
#------------CPU----------
BUS_SPEED=0

#CPU registers
pgm_count=np.uint16(0) #Program counter
stk_ptr=np.uint8(0) #stack pointer
inst_reg=np.uint8(0) #inst_regruction register
a_reg=np.uint8(0) #A register
x_reg=np.uint8(0) #X register
jmp=np.uint16(0) #pgm jump counter 
ret=np.uint16(0) #pgm return counter
hlt=0 #CPU Halt
rw=0 #read/write register
#system flags
z_flag=0

add_bus=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #16 Bit Address bus(Total 65536 memory locations)
data_bus=[0,0,0,0,0,0,0,0] #8 Bit Data bus

def pgm_counter(): #program counter
    global pgm_count
    pgm_count=pgm_count+1
def add_decode(add):
    global add_bus
    add_bus=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    c=add
    rem=0
    i=0
    while(i!=16):   
        rem=c%2
        c=c//2
        add_bus[i]=rem
        i=i+1
def add_encode():
    add=0
    for i in range(0,16):
        add=add+(add_bus[i]*(2**i))
    return add
def data_encode():
    data=0
    for i in range(0,8):
        data=data+(data_bus[i]*(2**i))
    return data
def data_decode(data):
    global data_bus
    data_bus=[0,0,0,0,0,0,0,0]
    c=data
    rem=0
    i=0
    while(i!=8):   
        rem=c%2
        c=c//2
        data_bus[i]=rem
        i=i+1
def bus():
    global rw
    global pgm_count
    global BUS_SPEED
    add_decode(pgm_count)
    ram(add_bus[15],add_bus[14],rw)
    #vc22(add_bus[13],not ((not add_bus[15]) and add_bus[14]),rw) #[Will be implemented in future]
    pla(add_bus[15],add_bus[14],add_bus[13],add_bus[12])
    rom(add_bus[15])
    time.sleep(1.0/BUS_SPEED)
def fetch():
    global inst_reg
    inst_reg=data_encode()
    execute()
def execute(): #inst_regruction execution
    global a_reg
    global x_reg
    global pgm_count
    global stk_ptr
    global inst_reg
    global rw
    global hlt
    global jmp
    global ret
    global z_flag

    #INSTRUCTIONS
    if(inst_reg==0xea): #NOP
        None
    if(inst_reg==0x14): #HLT
        hlt=1
    if(inst_reg==0x4c): #JMP
        pgm_count=pgm_count+1
        bus()
        jmp=data_encode()
        pgm_count=pgm_count+1
        bus()
        jmp=jmp*256+data_encode()
        pgm_count=jmp-1
    if(inst_reg==0xf0): #BEQ
        if(z_flag==1):
            z_flag=0
            pgm_count=pgm_count+1
            bus()
            jmp=data_encode()
            pgm_count=pgm_count+1
            bus()
            jmp=jmp*256+data_encode()
            pgm_count=jmp-1
        else:
            pgm_count=pgm_count+2
    if(inst_reg==0xc9): #CMP
        pgm_count=pgm_count+1
        bus()
        if(a_reg==data_encode()):
            z_flag=1
    if(inst_reg==0xe0): #CPX
        pgm_count=pgm_count+1
        bus()
        if(x_reg==data_encode()):
            z_flag=1
    if(inst_reg==0x20): #JSR
        pgm_count=pgm_count+1
        bus()
        jmp=data_encode()
        pgm_count=pgm_count+1
        bus()
        jmp=jmp*256+data_encode()
        ret=pgm_count
        rw=1
        pgm_count=(256+stk_ptr)
        data_decode(ret%256)
        bus()
        stk_ptr=stk_ptr+1
        pgm_count=(256+stk_ptr)
        data_decode(ret//256)
        bus()
        rw=0
        stk_ptr=stk_ptr+1
        pgm_count=jmp-1
    if(inst_reg==0x60): #RTS
        stk_ptr=stk_ptr-1
        pgm_count=(256+stk_ptr)
        bus()
        ret=data_encode()
        stk_ptr=stk_ptr-1
        pgm_count=(256+stk_ptr)
        bus()
        ret=ret*256+data_encode()
        pgm_count=ret
    if(inst_reg==0xaa): #TAX
        x_reg=a_reg
    if(inst_reg==0x8a): #TXA
        a_reg=x_reg
    if(inst_reg==0xa9): #LDA
        pgm_count=pgm_count+1
        bus()
        a_reg=data_encode()
    if(inst_reg==0xbd): #LDA
        pgm_count=pgm_count+1
        bus()
        jmp=data_encode()
        pgm_count=pgm_count+1
        bus()
        jmp=jmp*256+data_encode()
        ret=pgm_count
        pgm_count=jmp+x_reg
        bus()
        a_reg=data_encode()
        pgm_count=ret
        if(a_reg==0):
            z_flag=1
    if(inst_reg==0xad): #LDA
        pgm_count=pgm_count+1
        bus()
        jmp=data_encode()
        pgm_count=pgm_count+1
        bus()
        jmp=jmp*256+data_encode()
        ret=pgm_count
        pgm_count=jmp
        bus()
        a_reg=data_encode()
        pgm_count=ret
    if(inst_reg==0xa5): #LDA
        pgm_count=pgm_count+1
        bus()
        jmp=data_encode()
        ret=pgm_count
        pgm_count=jmp
        bus()
        a_reg=data_encode()
        pgm_count=ret
    if(inst_reg==0xa2): #LDX
        pgm_count=pgm_count+1
        bus()
        x_reg=data_encode()
    if(inst_reg==0x8d): #STA
        pgm_count=pgm_count+1
        bus()
        jmp=data_encode()
        pgm_count=pgm_count+1
        bus()
        jmp=jmp*256+data_encode()
        ret=pgm_count
        rw=1
        pgm_count=jmp
        data_decode(a_reg)
        bus()
        rw=0
        pgm_count=ret
    if(inst_reg==0x85): #STA
        pgm_count=pgm_count+1
        bus()
        jmp=data_encode()
        ret=pgm_count
        rw=1
        pgm_count=jmp
        data_decode(a_reg)
        bus()
        rw=0
        pgm_count=ret
    if(inst_reg==0x8e): #STX
        pgm_count=pgm_count+1
        bus()
        jmp=data_encode()
        pgm_count=pgm_count+1
        bus()
        jmp=jmp*256+data_encode()
        ret=pgm_count
        rw=1
        pgm_count=jmp
        data_decode(x_reg)
        bus()
        rw=0
        pgm_count=ret
    if(inst_reg==0x69): #ADD
       pgm_count=pgm_count+1
       bus()
       alu_add(data_encode())
    if(inst_reg==0xe9): #SUB
       pgm_count=pgm_count+1
       bus()
       alu_sub(data_encode())
    if(inst_reg==0x6d): #ADD
        pgm_count=pgm_count+1
        bus()
        jmp=data_encode()
        pgm_count=pgm_count+1
        bus()
        jmp=jmp*256+data_encode()
        ret=pgm_count
        pgm_count=jmp
        bus()
        alu_add(data_encode())
        pgm_count=ret
    if(inst_reg==0x65): #ADD
        pgm_count=pgm_count+1
        bus()
        jmp=data_encode()
        ret=pgm_count
        pgm_count=jmp
        bus()
        alu_add(data_encode())
        pgm_count=ret
    if(inst_reg==0xe8): #INX
        x_reg=x_reg+1
    if(inst_reg==0xca): #DEX
        x_reg=x_reg-1
    pgm_counter()    
def alu_add(operand):  #ALU Addition
    global a_reg
    a_reg=operand+a_reg
def alu_sub(operand):  #ALU Subtraction
    global a_reg
    a_reg=a_reg-operand
def reset():
    global pgm_count
    pgm_count=0xfffc
    bus()
    jmp=data_encode()
    pgm_count=0xfffd
    bus()
    jmp=jmp*256+data_encode()
    pgm_count=jmp
def control():
    global hlt
    reset()
    while(1):
        if(hlt==1):
            break
        else:
            bus()
            fetch()
def clock(speed):  #system clock
    global BUS_SPEED
    BUS_SPEED=speed
    control()
#-----------------------------------------      

def pla(i8,i7,i6,i5):
    io2=0
    io3=0
    if(i8==0 and i7==0 and i6==1 and i5==0):
        io2=1
        io3=1
    else:
        io2=0
        io3=0

    pla_devices(io2,io3)
        
def pla_devices(io2,io3):
    lcd162(add_bus[0],io2,data_encode())
    
#-------------Peripherals-----------------
def lcd162(RS,E,DATA):
    if(E==1):
        if(RS==1):
            print(int(DATA))
        else:
            print(chr(DATA),end="")
#--------------RAM module-----------------
def ram(cs,oe,rw):
    global data_bus
    if(cs==0 and oe==0):
        add=0
        for i in range(0,int(math.log(len(sram),2))):
            add=add+(add_bus[i]*(2**i))

        if(rw==0):
            data_bus=[0,0,0,0,0,0,0,0]
            rem=0
            a=sram[add]
            if(a==0):
                data_bus=[0,0,0,0,0,0,0,0]
            else:
                i=0
                while(i!=8):
                    rem=a%2
                    a=a//2
                    data_bus[i]=rem
                    i=i+1
            
        if(rw==1):
            data=0
            for i in range(0,8):
                data=data+(data_bus[i]*(2**i))
            sram[add]=data
#------------------------------------------------

#--------------------ROM module------------------
def rom(cs):
    global data_bus
    if(cs==1):
        data_bus=[0,0,0,0,0,0,0,0]
        add=0
        for i in range(0,int(math.log(len(prom),2))):
            add=add+(add_bus[i]*(2**i))
        rem=0
        a=prom[add]
        if(a==0):
            data_bus=[0,0,0,0,0,0,0,0]
        else:
            j=0
            while(j!=8):
                rem=a%2
                a=a//2
                data_bus[j]=rem
                j=j+1
#------------------------------------------------
                
#-------------------sys start--------------------
init_ram(16384) #16 KB of RAM used for optimal adressing
init_rom()
clock(1000000.0) #Frequency of clock is 1MHz
