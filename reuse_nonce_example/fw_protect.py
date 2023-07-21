"""
Firmware Bundle-and-Protect Tool
Bit Shifting Substitution Encryption
"""
import argparse
from pwn import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def protect_firmware(infile, outfile, version, message):
    # Load firmware binary from infile
    with open(infile, 'rb') as fp:
        firmware = fp.read()
    with open("secrets.txt","rb") as f:
        key = f.read(16)
        iv = f.read(10)
    cipher = AES.new(key, AES.MODE_CTR,nonce=iv)
    encrypted_firmware = cipher.encrypt(pad(firmware+message.encode()+b'\00', AES.block_size))

    # Pack version into two little-endian shorts
    metadata = p16(version) + p16(len(firmware))

    # Append firmware and message to metadata
    firmware_blob = metadata + encrypted_firmware

    # Write firmware blob to outfile
    with open(outfile, 'wb') as outfile:
        outfile.write(firmware_blob)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Firmware Update Tool')
    parser.add_argument("--infile", help="Path to the firmware image to protect.", required=True)
    parser.add_argument("--outfile", help="Filename for the output firmware.", required=True)
    parser.add_argument("--version", help="Version number of this firmware.", required=True)
    parser.add_argument("--message", help="Release message for this firmware.", required=True)
    args = parser.parse_args()
    protect_firmware(args.infile,args.outfile,int(args.version),args.message)
    #protect_firmware(infile="pure_firmware", outfile="encrypted_firmware", version=2, message="new release")
    #protect_firmware(infile="null_firmware", outfile="encrypted_null", version=2, message="new release")