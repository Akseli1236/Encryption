

from Crypto.Cipher import AES
from timeit import default_timer as timer
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

key = get_random_bytes(32)


def encryption(text):
    timer_e0 = timer()
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(text.encode(), AES.block_size))
    timer_e1 = timer()
    return ciphertext, cipher.iv, timer_e0, timer_e1


def decryption(ciphertext, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode()


def main():

    ciphertext, iv, timer_e0, timer_e1 = encryption(input('Enter a secret message: '))

    timer_d0 = timer()
    plaintext = decryption(ciphertext, iv)
    timer_d1 = timer()

    print(f"Generated key {key.hex()}, {iv.hex()}\n")
    print(f"Here is the ciphertext: {ciphertext.hex()}")
    print(f"Time to encode: {(timer_e1 - timer_e0)*1000} ms\n")

    print(f"Here is the plaintext: {plaintext}")
    print(f"Time to decode: {(timer_d1 - timer_d0)*1000} ms")

if __name__ == '__main__':
    main()
