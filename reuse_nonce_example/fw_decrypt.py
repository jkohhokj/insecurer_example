"""
Firmware Bundle-and-Protect Tool
Bit Shifting Substitution Decryption
"""
import argparse
from pwn import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def decrypt_firmware(infile, outfile):
    # Load firmware binary from infile
    with open(infile, 'rb') as fp:
        full_firmware = fp.read()
    with open("secrets.txt","rb") as f:
        key = f.read(16)
        iv = f.read(10)
    
    version = u16(full_firmware[0:2])

    size = u16(full_firmware[2:4])
    
    
    
    encrypted_firmware = full_firmware[4:]
    BLOCK_SIZE = AES.block_size
    cipher = AES.new(key, AES.MODE_CTR,nonce=iv)
    decrypted_firmware = unpad(cipher.decrypt(encrypted_firmware),AES.block_size)

    message = decrypted_firmware[size:]
    print(f"Version: {version}\tMessage: {message}")
    # Write firmware blob to outfile
    with open(outfile, 'wb+') as outfile:
        outfile.write(decrypted_firmware[:size])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Firmware Update Tool')
    parser.add_argument("--infile", help="Path to the firmware image to protect.", required=True)
    parser.add_argument("--outfile", help="Filename for the output firmware.", required=True)
    args = parser.parse_args()

    decrypt_firmware(infile=args.infile, outfile=args.outfile)
    #decrypt_firmware(infile="encrypted_firmware", outfile="decrypted_firmware")