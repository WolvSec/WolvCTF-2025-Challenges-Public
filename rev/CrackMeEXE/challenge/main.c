#include <windows.h>
#include <stdio.h>
#include <synchapi.h>
#include <processthreadsapi.h>
#include <stdlib.h>

//unsigned char shellcode[] = "\x31\xC0\x50\x68\x63\x61\x6C\x63\x89\xE3\x50\xB8\xC5\x1B\x86\x7C\xFF\xD0";

/*
flag = "wctf{Ann0y3d_Y3t?}"
key = "flag"
*/

// strlen
//unsigned char shellcode[] = "\x4d\x31\xd2\x42\x80\x3c\x11\x00\x74\x05\x49\xff\xc2\xeb\xf4\xc3";//"\x48\x31\xc0\x80\x79\x02\x44\x0f\x94\xc0\xc3";

// strlen == 18
//unsigned char shellcode[] = "\x4d\x31\xd2\x42\x80\x3c\x11\x00\x74\x05\x49\xff\xc2\xeb\xf4\x48\x83\xf8\x12\x74\x09\x48\xc7\xc0\x00\x00\x00\x00\xeb\x07\x48\xc7\xc0\x01\x00\x00\x00\xc3";

// strcmp to flag
//unsigned char shellcode[] = "\x55\x48\x89\xe5\x4d\x31\xd2\x42\x80\x3c\x11\x00\x74\x05\x49\xff\xc2\xeb\xf4\x49\x83\xfa\x12\x74\x09\x48\xc7\xc0\x01\x00\x00\x00\xc9\xc3\x68\x66\x6c\x61\x67\x49\x89\xe3\x41\x5c\x48\xc7\xc0\x3f\x7d\x00\x00\x50\x48\xb8\x30\x79\x33\x64\x5f\x59\x33\x74\x50\x48\xb8\x77\x63\x74\x66\x7b\x41\x6e\x6e\x50\x49\x89\xe4\x48\x31\xff\x49\x83\xfa\x00\x75\x00\x48\x89\xf8\xc9\xc3\x42\x8a\x5c\x11\xff\x48\x31\xc0\x43\x38\x5c\x14\xff\x0f\x95\xc0\x48\x01\xc7\x49\xff\xca\xeb\xd8";

// strcmp with xored flag
//unsigned char shellcode[] = "\x55\x48\x89\xe5\x4d\x31\xd2\x42\x80\x3c\x11\x00\x74\x05\x49\xff\xc2\xeb\xf4\x49\x83\xfa\x12\x74\x09\x48\xc7\xc0\x01\x00\x00\x00\xc9\xc3\x68\x66\x6c\x61\x67\x49\x89\xe3\x41\x53\x68\x59\x11\x00\x00\x48\xb8\x56\x15\x52\x03\x39\x35\x52\x13\x50\x48\xb8\x11\x0f\x15\x01\x1d\x2d\x0f\x09\x50\x49\x89\xe4\x48\x31\xff\x49\x83\xfa\x00\x75\x05\x48\x89\xf8\xc9\xc3\x42\x8a\x5c\x11\xff\x48\x31\xd2\x4c\x89\xd0\x48\xff\xc8\x49\xc7\xc5\x04\x00\x00\x00\x49\xf7\xf5\x41\x8a\x04\x13\x30\xc3\x48\x31\xc0\x43\x38\x5c\x14\xff\x0f\x95\xc0\x48\x01\xc7\x49\xff\xca\xeb\xc4";

// strcmp with xored flag; xored payload
unsigned char shellcode[] = "\x12\xa7\xe4\x21\xf3\xb0\xc6\xb6\x7a\x95\x5d\x7f\x8b\xed\x96\xe9\x45\x4d\x10\xcf\x7c\xdd\xf1\x31\xda\xf4\xfe\x8a\xea\x36\xbd\x22\xbf\x63\xcb\x27\x8a\x4f\xc6\xdf\xb2\x93\x10\x31\xed\x92\xc6\x49\xa4\x62\x7b\xfc\x46\xa3\x3a\x15\x50\x61\x5c\xc9\x05\x9c\xa7\xff\xf1\xd0\x80\x98\x68\x07\x82\xc5\x36\x54\x62\x37\xf9\xb4\xa7\x41\x46\x14\xcc\xd1\x0d\x9b\x1f\xb8\xbf\x5c\x41\xec\x50\x1c\x18\x5d\x57\x61\xf1\x81\xb5\xc3\xa7\x38\xcb\xd6\xa0\x14\x8a\x2c\xf9\x66\xb5\x39\xb9\xe8\xaa\xa7\x4c\x6a\xe3\x4c\x55\x43\x0c\x51\x52\xbf\x63\x07\xf9\xe2\xdf\xf3\xf5\xfd\x6a\x3c";



int main() {
    HANDLE k32 = GetModuleHandleA("kernel32.dll");
    if (!k32) {
        return -1;
    }

    FARPROC openProcess = GetProcAddress(k32, "OpenProcess");
    FARPROC virtualProtectEx = GetProcAddress(k32, "VirtualProtectEx");
    FARPROC writeProcessMemory = GetProcAddress(k32, "WriteProcessMemory");
    FARPROC virtualAllocEx = GetProcAddress(k32, "VirtualAllocEx");
    FARPROC isDebuggerPresent = GetProcAddress(k32, "IsDebuggerPresent");
    FARPROC checkRemoteDebuggerPresent = GetProcAddress(k32, "CheckRemoteDebuggerPresent");
    FARPROC getCurrentProcessId = GetProcAddress(k32, "GetCurrentProcessId");

    if (!openProcess || !virtualProtectEx || !writeProcessMemory || !virtualAllocEx || !isDebuggerPresent || !checkRemoteDebuggerPresent || !getCurrentProcessId) {
        return -1;
    }

    if (isDebuggerPresent()) {
        puts("Nice try");
        exit(-1);
    }

    DWORD procID = getCurrentProcessId();
    HANDLE procHandle = openProcess(PROCESS_ALL_ACCESS, FALSE, procID);
    if (!procHandle) {
        return -1;
    }

    PVOID remoteBuffer = virtualAllocEx(procHandle, NULL, (SIZE_T)sizeof(shellcode), MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
    if (!remoteBuffer) {
        return -2;
    }

    // Decrypt shellcode
    srand(13337);
    for (int i = 0; i < sizeof(shellcode); i++) {
        int val = rand() & 0xff;
        shellcode[i] = (shellcode[i] ^ val) & 0xff;
    }


    size_t bytesTransferred;
    int status = writeProcessMemory(procHandle, remoteBuffer, shellcode, sizeof(shellcode), &bytesTransferred);
    if (!status) {
        return -3;
    }

    DWORD oldProtect;
    status = virtualProtectEx(procHandle, remoteBuffer, sizeof(shellcode), PAGE_EXECUTE_READ, &oldProtect);
    if (!status) {
        return -4;
    }

    puts("What is the password?\n");

    BOOL check;
    status = checkRemoteDebuggerPresent(procHandle, &check);
    if (!status) {
        return -5;
    }

    if (check) {
        puts("NO CHEATING");
        exit(-1);
    }

    char buf[20] = { 0 };
    fgets(buf, sizeof(buf)-1, stdin);
    buf[strcspn(buf, "\n")] = '\0';

    long long int val = ((int(*)(long long int))remoteBuffer)(buf);

    if (val == 0) {
        puts("\nCORRECT!");
    }
    else {
        puts("\nWhat? no...");
    }

    return 0;
}
