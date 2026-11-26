// Box.asm  -  Roll 2501730399, K = 99
// Box: starts at row 99, 20 rows tall, 64 pixels (4 words) wide, from left edge.
// Start address = SCREEN + 32*99 = 16384 + 3168 = 19552
// While any key is pressed -> black box. When released -> box disappears.

(MAIN)
    @KBD
    D=M
    @BLACK
    D;JNE           // key pressed -> black
    @color
    M=0             // no key -> white (erase)
    @DRAW
    0;JMP
(BLACK)
    @color
    M=-1            // all 16 bits = 1
(DRAW)
    @19552
    D=A
    @addr
    M=D             // addr = first word of row 99
    @20
    D=A
    @rows
    M=D             // rows left = 20
(ROWLOOP)
    @color
    D=M
    @addr
    A=M
    M=D             // word 0
    A=A+1
    M=D             // word 1
    A=A+1
    M=D             // word 2
    A=A+1
    M=D             // word 3  (4 x 16 = 64 pixels)
    @32
    D=A
    @addr
    M=D+M           // next row
    @rows
    M=M-1
    D=M
    @ROWLOOP
    D;JGT
    @MAIN
    0;JMP
