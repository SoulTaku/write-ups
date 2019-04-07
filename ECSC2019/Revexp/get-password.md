
# ECSC 2019
**Author: Moga Tudor - alexmoga69@yahoo.com - SoulTaku**

## get-password (100): Revexp

### Proof of flag
>* ECSC{DAC553500B60BF700F56E456922104FA06BC144213ED2B58BEC2429F015242DB}

### Summary
>* Analyze the code in IDA > reverse the check_pw function > get the flag

### Proof of solving

At first I wanted to get a qemu to be able to run this binary, but after I fired up IDA Pro, I realized that it wasn't necessary. A quick look in IDA revealed that the binary read some input and then checked it against the check_pw function.

```C
memcpy(v4, &off_100001050, 0xA0uLL);
for ( i = 0; i < 96; ++i )
{
  if ( *(char *)(v4[i % 20] + 2 * (i / 10)) - *(char *)(a1 + i) != 1 )
  {
    v3 = 1;
    goto EXIT;
  }
}
```

At `&off_100001050` we had a matrix of chars. The program would check if each character in the string you passed is one smaller than the character in the array at a certain position. I quickly re-implemented this check in python, but my script was printing the character in the array minus one. [Keygen](https://github.com/SoulTaku/write-ups/blob/master/ECSC2019/Pwn/get.py).
