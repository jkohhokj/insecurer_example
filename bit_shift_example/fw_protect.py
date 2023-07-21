"""
Firmware Bundle-and-Protect Tool
Bit Shifting Substitution Encryption
"""
import argparse
from pwn import *

def protect_firmware(infile, outfile, version, message):
    # Load firmware binary from infile
    with open(infile, 'rb') as fp:
        firmware = fp.read()
        
    BLOCK_SIZE = 16
    CHUNK_SIZE = 1
    encrypted_firmware = b''
    for b in range(0,len(firmware),BLOCK_SIZE):
        block = firmware[b:b+BLOCK_SIZE]
        encrypted_block = b''
        for c in range(0,len(block),CHUNK_SIZE):
            encrypted_block += p8((u8(block[c:c+CHUNK_SIZE])+0xEF)&0xFF)
        encrypted_firmware += encrypted_block
    

    # Append null-terminated message to end of firmware
    firmware_and_message = encrypted_firmware + message.encode() + b'\00'

    # Pack version into two little-endian shorts
    metadata = p16(version) + p16(len(firmware))

    # Append firmware and message to metadata
    firmware_blob = metadata + firmware_and_message

    # Write firmware blob to outfile
    with open(outfile, 'wb') as outfile:
        outfile.truncate(0)
        outfile.write(firmware_blob)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Firmware Update Tool')
    parser.add_argument("--infile", help="Path to the firmware image to protect.", required=True)
    parser.add_argument("--outfile", help="Filename for the output firmware.", required=True)
    parser.add_argument("--version", help="Version number of this firmware.", required=True)
    parser.add_argument("--message", help="Release message for this firmware.", required=True)
    args = parser.parse_args()
    protect_firmware(args.infile,args.outfile,int(args.version),args.message)