
const readline = require("readline");
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

let { Builder, parseHex } = require('./wasm.js');

function win(key) {
    if (key === '🥺') {
        console.log("wctf{pr0l1f1c_1mp0rt3r}");
    }
}
globalThis.win = win;

rl.question(">>> ", (result) => {
    let wasmMod = new WebAssembly.Module(new Uint8Array(parseHex(result)));
    let instance = new WebAssembly.Instance(wasmMod, { 'i': globalThis });

    instance.exports.main();

    process.exit(0);
});

