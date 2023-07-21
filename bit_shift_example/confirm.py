with open("pure_firmware", "rb") as f:
    a = f.read()
with open("decrypted_firmware", "rb") as f:
    b = f.read()

print(a==b)