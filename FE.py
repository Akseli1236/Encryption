import os
import random

def generate_prime(bits):
    while True:
        candidate = random.getrandbits(bits)
        if is_prime(candidate):
            return candidate


def is_prime(candidate):
    if candidate <= 1:
        return False
    if candidate <= 3:
        return True
    if candidate % 2 == 0:
        return False

    for _ in range(5):
        a = random.randint(2, candidate - 2)
        if pow(a, candidate - 1, candidate) != 1:
            return False

    return True


L = 16
P = generate_prime(L)
Q = (P-1)//2
G = pow(random.randint(2, P - 2), 2, P)
X = random.randint(1, P - 1)
Y = pow(G, X, P)


msk = []
mpk = []

def power(a, b, c):
    x = 1
    y = a

    while b > 0:
        if b % 2 != 0:
            x = (x * y) % c;
        y = (y * y) % c
        b = int(b / 2)

    return x % c

for _ in range(L):
    X = random.randint(1, P - 1)
    msk.append(X)

    mpk_i = pow(G, X, P)
    mpk.append(mpk_i)


def generate_fe_key():
    skf = [msk[i] * y[i] % Q for i in range(len(y))]
    print(skf)
    return skf


x = input("Enter vector x (e.g., 1 2 3): ")

y = input("Enter vector y (e.g., 4 5 6): ")

def encrypt_ddh():

    ct = []
    s = power(power(G, X, Q), X, Q)
    for i in range(0, len(x)):
        ct.append(x[i])

    print("g^k used : ", P)
    for i in range(0, len(ct)):

        ct[i] = s * ord(ct[i])

    return ct, P


c, i = encrypt_ddh()


def decrypt_ddh():
    dr_msg = []
    h = power(P, X, Q)
    for i in range(0, len(x)):

        dr_msg.append(chr(int(c[i] / h)))

    return dr_msg


# Generate functional encryption key for inner-product
#skf = generate_fe_key()
decrypted_result = decrypt_ddh()
# Perform inner-product computation
#inner_product = sum(skf[i] * c[i] for i in range(len(skf)))




print(P, Q, G, X, Y, "\n", "\n", decrypted_result, "\n", c)