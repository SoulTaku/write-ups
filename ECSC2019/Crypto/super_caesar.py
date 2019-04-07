#!/usr/bin/python

lower = 17
upper = -2
c = 'YnuNmQPGhQWqCXGUxuXnFVqrUVCUMhQdaHuCIrbDIcUqnKxbPORYTzVCDBlmAqtKncpED'
flag = ''

for l in c:
    if l.islower():
        flag += chr(ord('a') + (ord(l) - ord('a') + lower) % 26)
    elif l.isupper():
        flag += chr(ord('A') + (ord(l) - ord('A') + upper) % 26)

print(flag)
