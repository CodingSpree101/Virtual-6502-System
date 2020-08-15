'''
A VC02 CPU 7 assembler for the VC25MIS architecture.

Written by Shreyan Dey.
Copyright(c)2020 Shreyan Dey.
All rights reserved.
Beta v6.0
Advanced Assembly Line Parsing Algorithm(AALPA) version: Beta v2.0
Last compiled on 15 August 2020

'''

import sys
import aalpa

file=sys.argv[1]
rom_size=int(sys.argv[2])
start=65536-rom_size

#file="pgm.asm"
#start=32768
#rom_size=32768


def init():
    print()
    print("VCMIS Assembler for VC02 CPU 7")
    print("Beta v5.1")
    print("Copyright(c)2020 Shreyan Dey")
    print()
    
#main assembler
def assemble():
    lines=list()
    labels=list()
    label_loc=list()
    variables=list()
    variable_value=list()
    code=bytearray(list())
    start=0
    
    instructions=[
        'LDA',
        'STA',
        "TAX",
        "TXA",
        "CMP",
        "LDX",
        "STX",
        "INX",
        "DEX",
        "CPX",
        "ADD",
        "SUB",
        "JMP",
        "BEQ",
        "JSR",
        "RTS",
        "NOP",
        "HLT",
    ]

    def seperate_into_tokens():
        aalpa.init()
        line=""
        for i in range(0,len(contents)):
            if(contents[i]=='\n'):
                lines.append(aalpa.parse(line))
                line=""
            elif(i+1==len(contents)):
                line=line+contents[i]
                lines.append(aalpa.parse(line))
                line=""
            else:
                line=line+contents[i]

    def get_label_addresses():
        for i in range(0,len(lines)):
            if(lines[i][0]!=''):
                labels.append(lines[i][0])

        for i in range(0,len(labels)):
            mem_loc=0
            for j in range(0,len(lines)):
                if(labels[i]==lines[j][0]):
                    label_loc.append(start+mem_loc)
                    break
                else:
                    if(lines[j][1]!=''):
                        if(lines[j][1][0]=='.'):
                            if(lines[j][2][0]=='\"' and lines[j][2][len(lines[j][2])-1]=='\"'):
                                size=len(lines[j][2].split('\"')[1])
                                if(lines[j][1]=='.ASCIIZ'):
                                    mem_loc=mem_loc+size+1
                                else:
                                    mem_loc=mem_loc+size
                            elif(lines[j][2][0]=='$'):
                                None
                        else:
                            mem_loc=mem_loc+1
                            if(lines[j][2]!=''):
                                if(lines[j][2][0]=='#'):
                                    data=int(lines[j][2].split('$')[1],16)
                                    if(data<256):
                                        mem_loc=mem_loc+1
                                elif(lines[j][2][0]=='$'):
                                    data=int(lines[j][2].split('$')[1],16)
                                    if(data<256):
                                        mem_loc=mem_loc+1
                                    else:
                                        mem_loc=mem_loc+2
                                elif(',' in lines[j][2]):
                                    if(lines[j][2].split(',')[0] in labels):
                                        mem_loc=mem_loc+2
                                elif(lines[j][2] in labels):
                                    mem_loc=mem_loc+2
                                else:
                                    mem_loc=mem_loc+2
    
    def convert_to_machine_code():
        global start
        for i in range(0,len(lines)):
            inst=lines[i][1]
            if(inst!=''):
                if(inst in instructions):
                    if(inst=='LDA'):
                        if(lines[i][2]!=''):
                            if(lines[i][2][0]=='#'):
                                data=int(lines[i][2].split('$')[1],16)
                                if(data<256):
                                    code.append(0xa9)
                                    code.append(data)
                            elif(lines[i][2][0]=='$'):
                                data=int(lines[i][2].split('$')[1],16)
                                if(data<256):
                                    code.append(0xa5)
                                    code.append(data)
                                else:
                                    code.append(0xad)
                                    code.append(data//256)
                                    code.append(data%256)
                            elif(',' in lines[i][2]):
                                if(lines[i][2].split(',')[0] in labels):
                                    data=label_loc[labels.index(lines[i][2].split(',')[0])]+start
                                    code.append(0xbd)
                                    code.append(data//256)
                                    code.append(data%256)
                            elif(lines[i][2] in labels):
                                data=label_loc[labels.index(lines[i][2])]+start
                                code.append(0xad)
                                code.append(data//256)
                                code.append(data%256)
                            elif(lines[i][2] in variables):
                                data=variable_value[variables.index(lines[i][2])]
                                if(data<256):
                                    code.append(0xa5)
                                    code.append(data)
                                else:
                                    code.append(0xad)
                                    code.append(data//256)
                                    code.append(data%256)
                    elif(inst=='STA'):
                        if(lines[i][2]!=''):
                            if(lines[i][2][0]=='$'):
                                data=int(lines[i][2].split('$')[1],16)
                                if(data<256):
                                    code.append(0x85)
                                    code.append(data)
                                else:
                                    code.append(0x8d)
                                    code.append(data//256)
                                    code.append(data%256)
                            elif(lines[i][2] in labels):
                                data=label_loc[labels.index(lines[i][2])]+start
                                code.append(0x8d)
                                code.append(data//256)
                                code.append(data%256)
                            elif(lines[i][2] in variables):
                                data=variable_value[variables.index(lines[i][2])]
                                if(data<256):
                                    code.append(0x85)
                                    code.append(data)
                                else:
                                    code.append(0x8d)
                                    code.append(data//256)
                                    code.append(data%256)
                    elif(inst=='LDX'):
                        if(lines[i][2]!=''):
                            if(lines[i][2][0]=='#'):
                                data=int(lines[i][2].split('$')[1],16)
                                if(data<256):
                                    code.append(0xa2)
                                    code.append(data)
                    elif(inst=='STX'):
                        if(lines[i][2]!=''):
                            if(lines[i][2][0]=='$'):
                                data=int(lines[i][2].split('$')[1],16)
                                code.append(0x8e)
                                code.append(data//256)
                                code.append(data%256)
                    elif(inst=='CMP'):
                        if(lines[i][2]!=''):
                            data=int(lines[i][2].split('$')[1],16)
                            if(data<256):
                                code.append(0xc9)
                                code.append(data)
                    elif(inst=='CPX'):
                        if(lines[i][2]!=''):
                            data=int(lines[i][2].split('$')[1],16)
                            if(data<256):
                                code.append(0xe0)
                                code.append(data)
                    elif(inst=='ADD'):
                        if(lines[i][2]!=''):
                            if(lines[i][2][0]=='#'):
                                data=int(lines[i][2].split('$')[1],16)
                                if(data<256):
                                    code.append(0x69)
                                    code.append(data)
                            elif(lines[i][2][0]=='$'):
                                data=int(lines[i][2].split('$')[1],16)
                                if(data<256):
                                    code.append(0x65)
                                    code.append(data)
                                else:
                                    code.append(0x6d)
                                    code.append(data//256)
                                    code.append(data%256)
                            elif(lines[i][2] in variables):
                                data=variable_value[variables.index(lines[i][2])]
                                if(data<256):
                                    code.append(0x65)
                                    code.append(data)
                                else:
                                    code.append(0x6d)
                                    code.append(data//256)
                                    code.append(data%256)
                    elif(inst=='SUB'):
                        if(lines[i][2]!=''):
                            if(lines[i][2][0]=='#'):
                                data=int(lines[i][2].split('$')[1],16)
                                if(data<256):
                                    code.append(0xe9)
                                    code.append(data)
                    elif(inst=='JMP'):
                        if(lines[i][2]!=''):
                            if(lines[i][2][0]=='$'):
                                data=int(lines[i][2].split('$')[1],16)
                                code.append(0x4c)
                                code.append(data//256)
                                code.append(data%256)
                            elif(lines[i][2] in labels):
                                data=label_loc[labels.index(lines[i][2])]+start
                                code.append(0x4c)
                                code.append(data//256)
                                code.append(data%256)
                    elif(inst=='BEQ'):
                        if(lines[i][2]!=''):
                            if(lines[i][2][0]=='$'):
                                data=int(lines[i][2].split('$')[1],16)
                                code.append(0xf0)
                                code.append(data//256)
                                code.append(data%256)
                            elif(lines[i][2] in labels):
                                data=label_loc[labels.index(lines[i][2])]+start
                                code.append(0xf0)
                                code.append(data//256)
                                code.append(data%256)
                    elif(inst=='JSR'):
                        if(lines[i][2]!=''):
                            if(lines[i][2][0]=='$'):
                                data=int(lines[i][2].split('$')[1],16)
                                code.append(0x20)
                                code.append(data//256)
                                code.append(data%256)
                            elif(lines[i][2] in labels):
                                data=label_loc[labels.index(lines[i][2])]+start
                                code.append(0x20)
                                code.append(data//256)
                                code.append(data%256)
                    elif(inst=='TAX'):
                        code.append(0xaa)
                    elif(inst=='TXA'):
                        code.append(0x8a)
                    elif(inst=='INX'):
                        code.append(0xe8)
                    elif(inst=='DEX'):
                        code.append(0xca)
                    elif(inst=='RTS'):
                        code.append(0x60)
                    elif(inst=='NOP'):
                        code.append(0xea)
                    elif(inst=='HLT'):
                        code.append(0x14)
                elif(inst[0]=='.'):
                    directive=lines[i][1].split('.')[1]
                    if(directive=='ASCIIZ'):
                        data=lines[i][2].split('\"')[1]
                        for i in range(0,len(data)):
                            if(data[i]=='\\' and data[i+1]=='n'):
                                code.append(ord('\n'))
                            elif(data[i-1]=='\\' and data[i]=='n'):
                                None
                            else:
                                code.append(ord(data[i]))
                        code.append(0x00)
                    elif(directive=='ORG'):
                        data=int(lines[i][2].split('$')[1],16)
                        start=data
                    elif(directive=='WORD'):
                        data=int(lines[i][2].split('$')[1],16)
                        code.append(data//256)
                        code.append(data%256)
                    elif(directive=='LET'):
                        var_name=lines[i][2].split('=')[0]
                        val=int(lines[i][2].split('=')[1].split('$')[1],16)
                        variables.append(var_name)
                        variable_value.append(val)
                else:
                    print("Error at line ",i+1,lines[i][1],"is an invalid instruction")
                    sys.exit()
        print("Compilation Succesful!")

    def write_to_file():
        rom=code+bytearray([0xea]*(rom_size-len(code)))               
        print("Writing to ROM:")
        rom[rom_size-4]=(65536-rom_size)//256
        rom[rom_size-3]=(65536-rom_size)%256
        print("ROM SIZE: ",rom_size," Bytes")
        print("Program occupies ",len(code)," Bytes")
        print("Remaining ",(rom_size-len(code))," Bytes")
        print("ROM start: ",hex(65536-rom_size))
        print()
        with open("VC28C.rom","wb") as out_file:
            out_file.write(rom)
        print("Done!")
    
    contents=""
    if(file.split('.')[1]=='asm'):
        with open(file, 'r') as f:
            contents=f.read()
        seperate_into_tokens()
        get_label_addresses()
        convert_to_machine_code()
        write_to_file()
    else:
        print("Only .asm files are supported")
#-------------------------------

init()
assemble()
