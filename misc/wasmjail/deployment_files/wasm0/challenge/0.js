
const readline = require("readline");
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

let { Builder, parseHex } = require('./wasm.js');

console.log("HII");
console.log("HII");
console.log("HII");

function win() {
    console.log("wctf{usu4lly_y0u_r3_r3v3r51n9_w45m_n0t_wr1t1ng_1t}");
}

let mod = new Builder();

// (type ;0; () -> ())
mod.addSection(1, [0x01, 0x60, 0x00, 0x00]);

// (func ;0; (import "i" "win") (type 0))
mod.addSection(2, [0x01, 0x01, 0x69, 0x03, 0x77, 0x69, 0x6e, 0x00, 0x00]);

// (func ;1; (type 0))...
mod.addSection(3, [0x01, 0x00])

// (func ;1; (export "main") (type 0))
mod.addSection(7, [0x01, 0x04, 0x6d, 0x61, 0x69, 0x6e, 0x00, 0x01])

rl.question(">>> ", (answer) => {
    mod.addSection(10, parseHex(answer));

    let wasmMod = new WebAssembly.Module(new Uint8Array(mod.data));
    let instance = new WebAssembly.Instance(wasmMod, { 'i': { win } });
    instance.exports.main();

    process.exit(0);
});

