
const readline = require("readline");
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

let { Builder, parseHex } = require('./wasm.js');
let flagArray = new TextEncoder().encode('wctf{0k4y_c4ll1n9_15_n1c3_but_w45m_h45_50_much_m0r3}');
console.log(flagArray.length);

let flag = new WebAssembly.Memory({ initial: 1, maximum: 1 });
let buf = new Uint8Array(flag.buffer);
for (let i = 0; i < flagArray.length; ++i) {
    buf[i] = flagArray[i];
}

function putc(s) {
    console.log(String.fromCharCode(s));
}

let mod = new Builder();

// (type ;0; (i32) -> ())
// (type ;1; () -> ())
mod.addSection(1, [0x02, 0x60, 0x01, 0x7f, 0x00, 0x60, 0x00, 0x00]);

// (memory (import "i" "flag") 64)
// (func ;0; (import "i" "putc") (type 0))
mod.addSection(2, [0x02, 0x01, 0x69, 0x04, 0x66, 0x6c, 0x61, 0x67, 0x02, 0x00, 0x01, 0x01, 0x69, 0x04, 0x70, 0x75, 0x74, 0x63, 0x00, 0x00]);

// (func ;1; (type 1))...
mod.addSection(3, [0x01, 0x01])

// (func ;1; (export "main") (type 0))
mod.addSection(7, [0x01, 0x04, 0x6d, 0x61, 0x69, 0x6e, 0x00, 0x01])

rl.question(">>> ", (answer) => {
    if (answer.length > 80) {
        console.log("too long :(");
        process.exit(1);
    }
    mod.addSection(10, parseHex(answer));

    let wasmMod = new WebAssembly.Module(new Uint8Array(mod.data));
    let instance = new WebAssembly.Instance(wasmMod, { 'i': { flag, putc } });
    instance.exports.main();

    process.exit(0);
});

