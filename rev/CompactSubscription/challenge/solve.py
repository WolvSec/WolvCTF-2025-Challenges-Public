# https://github.com/JacksonDonaldson/arcompact_be_ghidra
# ^ Ghidra support for big endian ARCompact

c0 = 0x12ac0256
c1 = 0x59a9d62b
c2 = 0x410ff20b
c3 = 0x2a318621


def calc_subscription(val):
    byteVals = val.to_bytes(4, "little")
    res = b""
    for byte in byteVals:
        byteRes = 0x00
        for bit in range(8):
            byteRes |= ((byte >> bit) & 1)<< ((bit - 2) % 8)
        res += byteRes.to_bytes(1, byteorder="little")
    return hex(int.from_bytes(res, byteorder = "little"))[2:]

key = [calc_subscription(c0), calc_subscription(c1), calc_subscription(c2), calc_subscription(c3)]

totalKey = ""
for i in range(4):
    totalKey += key[0][i*2:(i+1)*2] + key[1][i*2:(i+1)*2] + key[2][i*2:(i+1)*2] + key[3][i*2:(i+1)*2]

print("subscription: 00" + totalKey)

flag = [bytes.fromhex("f348f4f3"), bytes.fromhex("2d5ee7a9"), bytes.fromhex("0ff2cf9d"), bytes.fromhex("cc39ef35")]

def xor(b1, b2):
    return bytes([a^b for a,b in zip(b1, b2)])

print("flag: ", "".join([(xor(flag[i], bytes.fromhex(key[i]))).decode("utf-8") for i in range(4)]))

