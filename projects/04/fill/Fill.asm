// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(SETUP)
    @SCREEN
    D=A
    @pixel
    M=D    // set the first SCREEN address (16384)

    @KBD
    D=M
    @IFPRESS
    D;JGT
    @ELSE
    0;JMP
(IFPRESS)
    @color
    M=-1
    @ENDIF
    0;JMP
(ELSE)
    @color
    M=0
(ENDIF)

(FILL)
    @color
    D=M
    @pixel
    A=M
    M=D
    @pixel
    M=M+1

    @8192   // 256 rows * 32 words = 8192
    D=A
    @SCREEN
    D=D+A
    @pixel
    D=D-M

    @FILL
    D;JGT

    @SETUP
    0;JMP   // infinite loop
