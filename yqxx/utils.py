import base64
import random

from Crypto.Cipher import AES

BLOCK_SIZE = 16


def rds(len):
    chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678'
    return ''.join([random.choice(chars) for i in range(len)])


def pad(data):
    length = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + (chr(length)*length).encode()


def encrypt(message, passphrase):
    aes = AES.new(passphrase, AES.MODE_CBC, rds(16).encode())
    return base64.b64encode(aes.encrypt(pad(message)))
