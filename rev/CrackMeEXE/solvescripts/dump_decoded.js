// Frida script with specific address hook
(function() {
    console.log("[+] Specific address monitoring script loaded");
    
    // Function to dump memory
    function dumpMemory(address, size, prefix) {
        try {
            const bytes = Memory.readByteArray(address, size);
            console.log("[+] Memory dump preview of " + address + ":");
            console.log(hexdump(bytes, { length: Math.min(64, size) }));
            
            // Save to file
            const timestamp = new Date().getTime();
            const filename = prefix + "_" + address + "_" + timestamp + ".bin";
            const file = new File(filename, "wb");
            file.write(bytes);
            file.flush();
            file.close();
            console.log("[+] Full memory dump saved to " + filename);
            
            return bytes;
        } catch (e) {
            console.log("[-] Error dumping memory at " + address + ": " + e.message);
            return null;
        }
    }
    
    try {
        // Get the main module base address
        const mainModule = Process.getModuleByName(Process.enumerateModules()[0].name);
        console.log("[+] Main module base address: " + mainModule.base);
        
        // Target instruction address (absolute)
        let targetInstructionAddr = ptr("0x1400011b6");
        // Memory to dump (absolute)
        let memoryToDumpAddr = ptr("0x140005080");
        // Size to dump
        const dumpSize = 0x8b;
        
        console.log(`[+] Target instruction address: ${targetInstructionAddr}`);
        console.log(`[+] Memory to dump address: ${memoryToDumpAddr}`);
        console.log(`[+] Dump size: 0x${dumpSize.toString(16)} bytes`);
        
        // Validate if addresses are relative to module base
        if (targetInstructionAddr < mainModule.base || 
            targetInstructionAddr > mainModule.base.add(mainModule.size)) {
            console.log("[!] Warning: Target instruction address might be RVA, trying to adjust...");
            // Try to adjust to module base
            const targetInstructionRva = ptr("0x11b6");
            const adjustedTargetAddr = mainModule.base.add(targetInstructionRva);
            console.log(`[+] Adjusted target instruction address: ${adjustedTargetAddr}`);
            
            // Confirm with user via console log
            console.log("[!] Using adjusted target address. If this is incorrect, use absolute address in the script");
            
            // Set the adjusted address
            targetInstructionAddr = adjustedTargetAddr;
        }
        
        if (memoryToDumpAddr < mainModule.base || 
            memoryToDumpAddr > mainModule.base.add(mainModule.size)) {
            console.log("[!] Warning: Memory dump address might be RVA, trying to adjust...");
            // Try to adjust to module base
            const memoryToDumpRva = ptr("0x5080");
            const adjustedMemoryAddr = mainModule.base.add(memoryToDumpRva);
            console.log(`[+] Adjusted memory dump address: ${adjustedMemoryAddr}`);
            
            // Confirm with user via console log
            console.log("[!] Using adjusted memory address. If this is incorrect, use absolute address in the script");
            
            // Set the adjusted address
            memoryToDumpAddr = adjustedMemoryAddr;
        }
        
        // Perform initial memory dumps to check validity
        console.log("[+] Performing initial memory access test");
        try {
            // Just read a byte to verify memory is accessible
            Memory.readU8(targetInstructionAddr);
            Memory.readU8(memoryToDumpAddr);
            console.log("[+] Initial memory access test successful");
            
            // Dump initial memory state
            console.log("[+] Dumping initial memory state at target location");
            dumpMemory(memoryToDumpAddr, dumpSize, "initial_memory_state");
        } catch (e) {
            console.log("[-] Memory access test failed: " + e.message);
            console.log("[-] Please verify addresses are correct for this process");
        }
        
        // Set up instruction hook at the specific address
        try {
            console.log("[+] Setting up instruction hook at " + targetInstructionAddr);
            
            Interceptor.attach(targetInstructionAddr, {
                onEnter: function(args) {
                    console.log("[!!!] Target instruction at " + targetInstructionAddr + " is executing!");
                    
                    // Dump memory at specified address with specific size
                    console.log(`[+] Dumping 0x${dumpSize.toString(16)} bytes from ${memoryToDumpAddr}`);
                    dumpMemory(memoryToDumpAddr, dumpSize, "instruction_triggered_dump");
                    
                    // Dump register state
                    console.log("[+] Register state at instruction execution:");
                    try {
                        const context = this.context;
                        console.log("  RIP: " + context.rip);
                        console.log("  RAX: " + context.rax);
                        console.log("  RBX: " + context.rbx);
                        console.log("  RCX: " + context.rcx);
                        console.log("  RDX: " + context.rdx);
                        console.log("  RSI: " + context.rsi);
                        console.log("  RDI: " + context.rdi);
                        console.log("  RBP: " + context.rbp);
                        console.log("  RSP: " + context.rsp);
                        console.log("  R8:  " + context.r8);
                        console.log("  R9:  " + context.r9);
                        console.log("  R10: " + context.r10);
                        console.log("  R11: " + context.r11);
                        console.log("  R12: " + context.r12);
                        console.log("  R13: " + context.r13);
                        console.log("  R14: " + context.r14);
                        console.log("  R15: " + context.r15);
                        
                        // Also dump memory around instruction pointer for context
                        dumpMemory(context.rip.sub(0x10), 0x30, "instruction_context");
                        
                        // Dump some stack memory
                        dumpMemory(context.rsp, 0x50, "stack_at_instruction");
                    } catch (e) {
                        console.log("[-] Error getting register state: " + e.message);
                    }
                    
                    console.log("[+] Memory dump completed at instruction execution");
                }
            });
            
            console.log("[+] Successfully set up instruction hook");
        } catch (e) {
            console.log("[-] Error setting up instruction hook: " + e.message);
            console.log("[-] Details: " + e.stack);
            
            // Try an alternative approach using memory access monitoring
            console.log("[+] Trying alternative approach using memory access monitoring");
            try {
                MemoryAccessMonitor.enable({
                    base: targetInstructionAddr,
                    size: 1, // Just monitor the instruction byte
                    onAccess: function(details) {
                        if (details.operation === 'execute') {
                            console.log("[!!!] Execution detected at target address!");
                            console.log(`[+] Dumping 0x${dumpSize.toString(16)} bytes from ${memoryToDumpAddr}`);
                            dumpMemory(memoryToDumpAddr, dumpSize, "memory_monitor_triggered_dump");
                        }
                    }
                });
                console.log("[+] Memory access monitor set up successfully");
            } catch (e) {
                console.log("[-] Error setting up memory monitor: " + e.message);
                console.log("[-] Details: " + e.stack);
            }
        }
        
        console.log("[+] Script is now active");
    } catch (e) {
        console.log("[-] Critical error in script: " + e.message);
        console.log("[-] Error stack: " + e.stack);
    }
})();