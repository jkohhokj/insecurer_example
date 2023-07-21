from pwn import *
with open("encrypted_firmware", "rb") as f:
    a = f.read()
with open("encrypted_null", "rb") as f:
    b = f.read()
with open("pure_firmware", "rb") as f:
    c = f.read()
with open("decrypted_firmware","rb") as f:
    d = f.read()
print("Pure firmware == decrypted firmware: ",c==d)

print("Encrypted firmware ^ Encrypted null, Pure firmware")
for i in range(0,len(c),16):
    print(xor(a,b)[i+4:i+4+16],c[i:i+16])

print("Pure firmware, Decrypted firmware")
for i in range(0,len(c),16):
    print(c[i:i+16], d[i:i+16])
print(c[-16:], d[-16:])