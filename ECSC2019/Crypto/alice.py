#!/usr/bin/python

data    = open('Alice_replies.txt').read().split()
second  = [i[32:] for i in data]

# Calculate the second part of the flag

flag2 = ''
for i in range(32):
    valid = '1234567890abcdef'
    for j in range(16):
        valid = valid.replace(second[j][i], '')
    assert len(valid) == 1
    flag2 += valid


# Transpose the matrix

first = ['']
for i in range(32):
    for j in range(16):
        first[len(first)-1] += data[j][i]
    first.append('')

# Calculate the first part of the flag

flag1 = ''
for i in range(len(first)):
    for j in range(len(first[i])):
        if first[i].count(first[i][j]) == 1:
            flag1 += first[i][j]
            break

print('ECSC{' + flag1 + flag2 + '}')
