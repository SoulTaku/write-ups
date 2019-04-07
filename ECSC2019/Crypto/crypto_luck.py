#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from pwn import *
import hashlib
import time

context.update(arch='i386')
exe = './path/to/binary'

host = args.HOST or '37.128.230.46'
port = int(args.PORT or 50041)

def local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

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

def crack(h):
    for i in xrange(1000000000):
        if hashlib.sha1(str(i).encode()).hexdigest()[:6] == h:
            return str(i)

gdbscript = '''
continue
'''.format(**locals())

# -- Exploit goes here --

io = start()

for i in range(10):
    time.sleep(10)
    target = io.recvline().strip()
    log.info('Cracking: ' + target)
    h = crack(target)
    log.info('Found: ' + h)
    io.sendline(h)

io.interactive()

