import random

# To find gcd of two numbers
def gcd(a, b):
    if a < b:
        return gcd(b, a)
    elif a % b == 0:
        return b
    else:
        return gcd(b, a % b)

# For key generation, i.e., large random number
def gen_key(q):
    key = random.randint(pow(10, 20), q)
    while gcd(q, key) != 1:
        key = random.randint(pow(10, 20), q)
    return key

def power(a, b, c):
    x = 1
    y = a
    while b > 0:
        if b % 2 == 0:
            x = (x * y) % c
        y = (y * y) % c
        b = int(b / 2)
    return x % c

def generate_keys(L, P, G):
    msk = []
    mpk = []
    for _ in range(L):
        X = random.randint(1, P - 1)
        msk.append(X)

        mpk_i = power(G, X, P)
        mpk.append(mpk_i)
    return msk, mpk

# For asymmetric encryption
def encryption(msg, q, h, p, mpk):
    ct = []
    k = gen_key(q)

    for i in range(0, len(msg)):
        ct.append(msg[i])
    print("g^k used = ", p)
    for i in range(0, len(ct)):
        s = power(h, mpk[i], q)
        ct[i] = s * ord(ct[i])
    return ct

# For decryption
def decryption(ct, p, key, q, mpk):
    pt = []

    for i in range(0, len(ct)):
        h = power(p, mpk[i], q)
        pt.append(chr(int(ct[i] / h)))
    return pt

msg = input("Enter message: ")
P = random.randint(pow(10, 20), pow(10, 50))
q = (P-1) // 2
g = random.randint(2, q)
key = gen_key(q)
h = power(g, key, q)
print("g used =", g)
print("g^a used =", h)

L = len(msg)  # You can change this to the desired number of keys

msk, mpk = generate_keys(L, P, g)

ct = encryption(msg, q, h, P, mpk)

print("Original Message =", msg)
print("Encrypted Message =", ct)

pt = decryption(ct, P, key, q, msk)
d_msg = ''.join(pt)
print("Decrypted Message =", d_msg)
