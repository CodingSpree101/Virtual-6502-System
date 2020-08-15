IT SHOULD BE NOTED THAT THIS CODE IS STILL IN BETA SO BUGS MAY OCCUR.

This is a system that is based on the Commodore VIC 20 computer but works differently.
Codes written for the real 6502 will work here but i slight modification has to be done to the operands since this VCPU follows Big Endian format while the real CPU followed the Little Endian format.
The CPU still lacks a lot of features of the Original 6502 but it will be all added in the future.

Current with the default settings it has 16 KB of RAM and 1 KB of ROM.
The following is the current memory map:

Zero Page:           0x0000 - 0x00FF ;
Stack:               0x0000 - 0x01FF ;
General Purpose RAM: 0x0200 - 0x1FFF ;
PLA:                 0x2000 - 0x2FFF ;
VC22(Unimplemented): 0x6000 - 0x7FFF ;
ROM:                 0xFC00 - 0xFFFF 

The opcodes for the cpu are given in the opcodes.txt file.
A VC28C.rom file should be present in the same folder which contains the code for the CPU to execute. It can be either handbuilt using machine object code or the VC02 Assembler can be used.

To use the VC02 Assembler , create an assembly source file with the code the open the command prompt and navigate to the folder and write the following command:
$ python vcasm.py [filename].asm [rom size]

A fibonacci.asm file is provided for testing.


 It should be noted the assembler is also in BETA so bugs may occur.

Minimum Requirements:
Python 3,
Numpy
