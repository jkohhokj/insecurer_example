from pwn import *
import os
from datetime import date
with open("pure_firmware", 'wb') as f:
    for i in range(640):
        f.write(p8(i*17%64))

with open("null_firmware", 'wb') as f:
    for i in range(640):
        f.write(p8(0))


def generate_keys(infile):
    with open(infile, "wb") as f:
        key = os.urandom(16)
        iv = bytes(str(date.today()),'utf-8')
        f.write(key)
        f.write(iv)

generate_keys("secrets.txt")