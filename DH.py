import random
import hashlib

def public_key(a_private, b_private, g_value, p_value):
    A_public = g_value ** a_private % p_value
    B_public = g_value ** b_private % p_value
    return A_public, B_public

def shared_key(public, private, p_value):
    shared_secret = public ** private % p_value
    return shared_secret

if __name__ == "__main__":
    g = 7
    p = 11
    #A_private = random.randint(10, p-1)
    A_private = 6
    #B_private = random.randint(10, p-1)
    B_private = 9
    A_public, B_public = public_key(A_private, B_private, g, p)
    shared_secret_A = shared_key(B_public, A_private, p)
    shared_secret_B = shared_key(A_public, B_private, p)
    hashed_secret = hashlib.sha256(str(shared_secret_B).encode('utf-8')).digest()
    key = hashed_secret[:16]
    print(f"p: {p} g: {g}")
    print(f"Alice's private key: {A_private} and public key: {A_public}")
    print(f"Bob's private key: {B_private} and public key: {B_public}")
    print(f"Shared value: {shared_secret_A} and hashed key: {key}")

    message = input("Give a message: ")
    encrypted_message = []
    for i in range(len(message)):
        encrypted_char = ord(message[i]) ^ key[i % 16]
        encrypted_message.append(encrypted_char)
    print("Encrypted:", encrypted_message)

    decrypted_message = []
    for i in range(len(encrypted_message)):
        decrypted_char = encrypted_message[i] ^ key[i % 16]
        decrypted_message.append(chr(decrypted_char))

    decrypted_message = "".join(decrypted_message)
    print("Decrypted:", decrypted_message)
