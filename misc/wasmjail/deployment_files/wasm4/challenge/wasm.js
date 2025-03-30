
let isEven = require('is-even');

function leb128(n) {
    let result = [];
    do {
        result.push((n & 0x7f) | 0x80);
        n >>= 7;
    } while (n)
    result[result.length - 1] &= 0x7f;
    return result;
}

class Builder {
    constructor() {
        this.data = [0x00, 0x61, 0x73, 0x6d, 0x01, 0x00, 0x00, 0x00];
    }

    addSection(id, section) {
        this.data.push(id);
        this.data.push(...leb128(section.length));
        this.data.push(...section);
    }
}

// node doesn't support Uint8Array.fromHex :(
function parseHex(answer) {
    // javascript developers try not to write literally anything
    // into a package challenge IMPOSSIBLE
    if (!isEven(answer.length)) {
        console.log("odd");
        process.exit(1);
    }
    let result = [];
    for (let i = 0; i < answer.length; i += 2) {
        result.push(parseInt(answer.substring(i, i+2), 16));
    }
    return result;
}

module.exports = { Builder, parseHex }

