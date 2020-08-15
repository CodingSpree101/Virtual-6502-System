;Variable declarations
	.LET A=$0200
	.LET B=$0201
	.LET C=$0202
	.LET LCHAR=$2000 ;address to print character
	.LET LINT=$2001 ;address to print data
SETUP:
	JSR TITLE
	LDX #$00
	LDA #$00
	STA A
	LDA #$01
	STA B
	LDA #$00
	STA C
	LDA A
	STA LINT
	INX
	LDA B
	STA LINT
	INX
LOOP:
	ADD A
	STA C
	STA LINT
	INX
	LDA B
	STA A
	LDA C
	STA B
	CPX $0E
	BEQ END
	JMP LOOP
END: HLT
TITLE:
	LDX #$00
TLOOP:
	LDA MSG,X
	BEQ BACK
	STA LCHAR
	INX
	JMP TLOOP
BACK: RTS
MSG: .ASCIIZ "The Fibonacci Series\n"