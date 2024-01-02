from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from timeit import default_timer as timer
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

user_name = input("Enter user name: ")
# Generate ECC key pair
private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
public_key = private_key.public_key()

# Serialize private key to PEM format and save it to a file
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

with open(f'{user_name}_ECC_private_key.pem', 'wb') as private_key_file:
    private_key_file.write(private_pem)

# Serialize public key to PEM format and save it to a file
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

with open(f'{user_name}_ECC_public_key.pem', 'wb') as public_key_file:
    public_key_file.write(public_pem)

# Message to be encrypted
f = open("text.txt", "r")
plaintext = f.read().encode()

# Load recipient's public key from file
with open(f'{user_name}_ECC_public_key.pem', 'rb') as key_file:
    recipient_public_key = serialization.load_pem_public_key(key_file.read(), backend=default_backend())

# Generate shared secret
shared_secret = private_key.exchange(ec.ECDH(), recipient_public_key)

# Derive encryption key from shared secret
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    iterations=100000,
    salt=os.urandom(16),
    length=32,
    backend=default_backend()
)
encryption_key = kdf.derive(shared_secret)
print(plaintext.decode(), "\n")
# Encrypt the message
timer_e0 = timer()
cipher = Cipher(algorithms.AES(encryption_key), modes.CFB(os.urandom(16)), backend=default_backend())
encryptor = cipher.encryptor()
ciphertext = encryptor.update(plaintext) + encryptor.finalize()
timer_e1 = timer()

# Print the ciphertext (binary)

print("Ciphertext:", ciphertext.hex())
print(f"Time to encode: {(timer_e1 - timer_e0) * 1000} ms\n")

timer_d0 = timer()
decryptor = cipher.decryptor()
decrypted_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
timer_d1 = timer()
print("Decoded plaintext:\n", decrypted_plaintext.decode())
print(f"Time to decode: {(timer_d1 - timer_d0) * 1000} ms")