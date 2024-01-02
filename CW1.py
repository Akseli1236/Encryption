import binascii
import hashlib

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def compute_sha256_hash(word):
    sha256 = hashlib.sha256()
    sha256.update(word.encode('utf-8'))
    return sha256.hexdigest()

def encrypt_aes(data, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    return ciphertext, cipher.iv  # Return both ciphertext and IV

keyword = compute_sha256_hash("cranberry cola")
keyword_key = hashlib.sha256(
                (keyword + str(0)).encode('utf-8')).hexdigest()
print(keyword[:11])
print(keyword_key)

csp_keywords_address = hashlib.sha256(
                (keyword_key + str(29)).encode('utf-8')).hexdigest()
print(csp_keywords_address)

key = "38413544454336383631353138354144"
bytes_data = binascii.unhexlify(key)
cipher = AES.new(bytes_data, AES.MODE_ECB)
data = "important_info.txt" + str(29)

padded_data = pad(data.encode('utf-8'),AES.block_size)
ciphertext = cipher.encrypt(padded_data)
hex_cipher = binascii.hexlify(ciphertext).decode('utf-8')
print(hex_cipher[:11])