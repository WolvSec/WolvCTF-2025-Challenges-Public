//sudo apt install libseccomp-dev
//g++ vuln.cpp -l seccomp -fno-stack-protector -o drywall
// g++ (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0
// using the libc in the directory
#include <seccomp.h>
#include <stdio.h>
#include <stdlib.h>

typedef void * scmp_filter_ctx;

static char name[30];

void gift(){
    asm ("pop %rdx; ret;");
    asm ("pop %rax; ret;");
    asm ("syscall; ret;");
}

int main(){
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

    scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_ALLOW); //SCMP_ACT_KILL

    
    // seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit),0);
    // seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read),0);
    // seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write),0);
    // seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(rt_sigreturn),0);
    // seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(access),0);
    // seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(arch_prctl),0);
    // seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group),0);
    // seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(prctl),0);
    // seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(syscall),0);
    // seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(seccomp),0);

    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(execve),0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(open),0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(execveat),0);
    //seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(write),0);
    //seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(read),0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(readv),0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(writev),0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(process_vm_readv),0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(process_vm_writev),0);


    seccomp_load(ctx);
    
    char buf[256];
    puts("What is your name, epic H4x0r?");
    fgets(name, 30, stdin);

    printf("Good luck %s <|;)\n", name);
    printf("%p\n",main);
    fgets(buf, 0x256, stdin);

    return 0;
}
