import base64
import hashlib
import random

from Crypto import Random
from Crypto.Cipher import AES


class AESCipher:

    def __init__(self, key):
        self.bs = AES.block_size
        self.key = key.encode('utf-8')

    # def encrypt(self, raw):
    #     raw = self._pad(raw)
    #     iv = Random.new().read(AES.block_size)
    #     cipher = AES.new(self.key, AES.MODE_CBC, iv)
    #     return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def encrypt(self, plain_text, iv):
        cipher = AES.new(self.key, AES.MODE_CBC, iv.encode('utf-8'))
        content_padding = self.aes_pkcs5_padding(plain_text, self.bs)
        encrypt_bytes = cipher.encrypt(content_padding.encode('utf-8'))
        return encrypt_bytes

    def aes_pkcs5_padding(self, cipher_text, block_size):
        padding_size = len(cipher_text) if (len(cipher_text) == len(
            cipher_text.encode('utf-8'))) else len(cipher_text.encode('utf-8'))
        padding = block_size - padding_size % block_size
        if padding < 0:
            return None
        padding_text = chr(padding) * padding
        return cipher_text + padding_text



    #
    # def decrypt(self, enc):
    #     enc = base64.b64decode(enc)
    #     iv = enc[:AES.block_size]
    #     cipher = AES.new(self.key, AES.MODE_CBC, iv)
    #     return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    # def _pad(self, s):
    #     return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)
    #
    # @staticmethod
    # def _unpad(s):
    #     return s[:-ord(s[len(s) - 1:])]
