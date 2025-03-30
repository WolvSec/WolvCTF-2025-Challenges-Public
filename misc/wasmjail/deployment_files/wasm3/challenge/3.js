
const readline = require("readline");
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

let { Builder, parseHex } = require('./wasm.js');

function win() {
    console.log("wctf{3xpl1c1t_t41l_c4ll5}");
}

let mod = new Builder();

// (type ;0; () -> ())
mod.addSection(1, [0x01, 0x60, 0x00, 0x00]);

// (func ;0; (import "i" "a") (type 0))
// (func ;1; (import "i" "a") (type 0))
// (func ;2; (import "i" "a") (type 0))
// (func ;3; (import "i" "win") (type 0))
mod.addSection(2, [0x04, 0x01, 0x69, 0x01, 0x61, 0x00, 0x00, 0x01, 0x69, 0x01, 0x61, 0x00, 0x00, 0x01, 0x69, 0x01, 0x61, 0x00, 0x00, 0x01, 0x69, 0x03, 0x77, 0x69, 0x6e, 0x00, 0x00]);

// (func ;4; (type 0))...
mod.addSection(3, [0x01, 0x00])

// (func ;4; (export "main") (type 0))
mod.addSection(7, [0x01, 0x04, 0x6d, 0x61, 0x69, 0x6e, 0x00, 0x04])

rl.question(">>> ", (answer) => {
    if (/03/.test(answer)) {
        console.log("no");
        process.exit(1);
    }
    if (/^(..)*10/.test(answer)) {
        console.log("no");
        process.exit(1);
    }

    mod.addSection(10, parseHex(answer));

    let wasmMod = new WebAssembly.Module(new Uint8Array(mod.data));
    let instance = new WebAssembly.Instance(wasmMod, { 'i': { win, a: () => {} } });
    instance.exports.main();

    process.exit(0);
});

