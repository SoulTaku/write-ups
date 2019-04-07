
# ECSC 2019
**Author: Moga Tudor - alexmoga69@yahoo.com - SoulTaku**

## super_caesar (250): Crypto

### Proof of flag
>* ECSC{BGtSheIosNMPWRqTABZcdYhkIetgCB}

### Summary
>* find the two key > shift

### Proof of solving

While trying different shifts on the first string, with a shift of +17 I got the string "start", while on the last string with a shift of -2 I got "STOP". I realized that the first was lowercase while the last was uppercase, so I tried to decrypt the lowercase letters with a shift of 17 and the uppercase with a shift of -2. Final [solver](https://github.com/SoulTaku/write-ups/blob/master/ECSC2019/Crypto/super_caesar.py)
