
# ECSC 2019
**Author: Moga Tudor - alexmoga69@yahoo.com - SoulTaku**

## guessing-game (100): Revexp

### Proof of flag
>* ECSC{9120848337A9760DDAE532BAF3D7D8E7032DFFFE6DD3B323A5F5CA0455B9C79C}

### Summary
>* Dynamic analysis to find variables on stack > leak variables and get flag

### Proof of solving

My first try was to implement a rand that would take the same seed as the binary an produce the three numbers, but I finally solved it using the format string exploit. When you connect it asks for a name which is echoed back as the first parameter of the printf function, thus leaking the stack. After playing a bit in GDB i found the 3 variables on the stack. At first I couldn't find the third one because I was using %x to print the stack, after I switched to %p I found the third too. Exploit [script](https://github.com/SoulTaku/write-ups/blob/master/ECSC2019/Pwn/a.py).
