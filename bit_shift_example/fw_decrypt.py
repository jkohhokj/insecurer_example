"""
Firmware Bundle-and-Protect Tool
Bit Shifting Substitution Decryption
"""
import argparse
import struct
from pwn import *


def decrypt_firmware(infile, outfile):
    # Load firmware binary from infile
    with open(infile, 'rb') as fp:
        full_firmware = fp.read()
    
    
    version = u16(full_firmware[0:2])

    size = u16(full_firmware[2:4])
    
    message = full_firmware[4+size:]
    
    encrypted_firmware = full_firmware[4:4+size]

    BLOCK_SIZE = 16
    CHUNK_SIZE = 1
    decrypted_firmware = b''
    for b in range(0,len(encrypted_firmware),BLOCK_SIZE):
        block = encrypted_firmware[b:b+BLOCK_SIZE]
        decrypted_block = b''
        for c in range(0,len(block),CHUNK_SIZE):
            #print(block[c:c+CHUNK_SIZE])
            #print(u16(block[c:c+CHUNK_SIZE])-0xBEEF)
            decrypted_block += p8((u8(block[c:c+CHUNK_SIZE])-0xEF)&0xFF)
        decrypted_firmware += decrypted_block


    print(f"Version: {version}\tMessage: {message}")
    # Write firmware blob to outfile
    with open(outfile, 'wb') as outfile:
        outfile.write(decrypted_firmware)


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Firmware Update Tool')
    # parser.add_argument("--infile", help="Path to the firmware image to protect.", required=True)
    # parser.add_argument("--outfile", help="Filename for the output firmware.", required=True)
    # args = parser.parse_args()

    #decrypt_firmware(infile=args.infile, outfile=args.outfile)
    decrypt_firmware(infile="encrypted_firmware", outfile="decrypted_firmware")