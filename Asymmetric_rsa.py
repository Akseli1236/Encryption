from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import os
from timeit import default_timer as timer
import hashlib



def generate_rsa_key_pair(user_name):
    key = RSA.generate(2048)

    private_key = key.export_key()
    with open(f'{user_name}_Private_Key.pem', 'wb') as private_key_file:
        private_key_file.write(private_key)

    public_key = key.publickey().export_key()
    with open(f'{user_name}_Public_Key.pem', 'wb') as public_key_file:
        public_key_file.write(public_key)


# Function to encrypt text with RSA public key
def encrypt_text_with_rsa_public_key(public_key_file, plaintext):
    with open(public_key_file, 'rb') as key_file:
        public_key = RSA.import_key(key_file.read())

    cipher = PKCS1_OAEP.new(public_key)
    ciphertext = cipher.encrypt(plaintext.encode())

    return ciphertext


# Function to decrypt ciphertext with RSA private key
def decrypt_ciphertext_with_rsa_private_key(private_key_file, ciphertext):
    with open(private_key_file, 'rb') as key_file:
        private_key = RSA.import_key(key_file.read())

    cipher = PKCS1_OAEP.new(private_key)
    plaintext = cipher.decrypt(ciphertext).decode()

    return plaintext

def compute_sha256_hash(filename):
    # Initialize SHA-256 hash object
    sha256_hash = hashlib.sha256()

    # Read and update hash string value in blocks of 4K
    with open(filename, "rb") as file:
        while True:
            data = file.read(4096)  # Read 4K at a time
            if not data:
                break
            sha256_hash.update(data)

    # Get the hexadecimal representation of the hash
    return sha256_hash.hexdigest()

def verify_integrity(filename, expected_hash):
    # Compute the hash of the file
    computed_hash = compute_sha256_hash(filename)

    # Verify if the computed hash matches the expected hash
    if computed_hash == expected_hash:
        print("File integrity verified. The hashes match.\n")
    else:
        print("File integrity verification failed. The hashes do not match.\n")


def sign_message(private_key_file, message_file):
    with open(private_key_file, 'rb') as key_file:
        private_key = RSA.import_key(key_file.read())

    with open(message_file, 'rb') as message_file:
        message = message_file.read()

    hash_obj = SHA256.new(message)
    signature = pkcs1_15.new(private_key).sign(hash_obj)

    return signature


def verify_signature(public_key_file, message_file, signature):
    with open(public_key_file, 'rb') as key_file:
        public_key = RSA.import_key(key_file.read())

    with open(message_file, 'rb') as message_file:
        message = message_file.read()

    hash_obj = SHA256.new(message)

    try:
        pkcs1_15.new(public_key).verify(hash_obj, signature)
        return True  # Signature is valid
    except (ValueError, TypeError):
        return False  # Signature is invalid

# Main program
if __name__ == "__main__":
    user_name = input("Name: ")
    print(f"Using {user_name}_Pivate_Key.pem")

    file = input("Enter file: ")

    # Generate RSA key pair based on user's chosen name
    #generate_rsa_key_pair(user_name)

    # Create a text paragraph for encryption
    computed_hash = compute_sha256_hash(file)

    f = open(file, "r")
    plaintext = f.read()
    print(plaintext)
    # Encrypt the text with the user's public key
    timer_e0 = timer()
    ciphertext = encrypt_text_with_rsa_public_key(
        f'{user_name}_Public_Key.pem', plaintext)
    timer_e1 = timer()


    print("\nEncryption completed.")
    print("Ciphertext:", ciphertext.hex())
    print(f"Time to encode: {(timer_e1 - timer_e0) * 1000} ms\n")

    # Decrypt the ciphertext with the user's private key
    timer_d0 = timer()
    decrypted_text = decrypt_ciphertext_with_rsa_private_key(
        f'{user_name}_Private_Key.pem', ciphertext)
    timer_d1 = timer()

    print("\nDecryption completed.")
    print("Decrypted Text:", decrypted_text)
    print(f"Time to decode: {(timer_d1 - timer_d0) * 1000} ms")

    signature = sign_message(f'{user_name}_Private_Key.pem', "text.txt")
    print("\nSignature:", signature.hex())

    print(f"Sender public key {user_name}.Public.Key.pem")
    verification_result = verify_signature(f'{user_name}_Public_Key.pem',
                                           "text.txt", signature)
    if verification_result:
        print("\nSignature is valid.")
    else:
        print("\nSignature is invalid.")

