import base64

flag = "wctf{bA5E_tWo_p0W_s!X}"
encoded = flag.encode('utf-8')
for _ in range(17):
    encoded = base64.b64encode(encoded)
result = encoded.decode('utf-8')
print("encoded flag:", result)

encoded_flag = result
decoded = encoded_flag.encode('utf-8')
for _ in range(17):
    decoded = base64.b64decode(decoded)
result = decoded.decode('utf-8')
print("decoded flag:", result)