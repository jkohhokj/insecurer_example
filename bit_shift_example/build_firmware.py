import struct
with open("pure_firmware", 'wb') as f:
    for i in range(640):
        f.write(struct.pack('<H',i*3%64))