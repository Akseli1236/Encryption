import binascii


def change_to_be_hex(s):
    return hex(int(s, base=16))


m1_binary = "LIFEISLIKEABOXOFCHOCOLATES"
c1_binary = "CXGDXNIPWXYXTONWQTCVCFXKCY"
c2_binary = "PDVMTQBYWGMSBYZKMAIPWFIXCZ"


def xor_two_str(a,b):
    return ''.join([hex(ord(a[i%len(a)]) ^ ord(b[i%(len(b))]))[2:] for i in range(max(len(a), len(b)))])

def xor_two_hex_strings(str1, str2):
    # Remove the '0x' prefix from the hexadecimal strings, if present
    str1 = str1.lstrip('0x')
    str2 = str2.lstrip('0x')

    # Make sure the two strings have the same length by zero-padding the shorter one
    max_len = max(len(str1), len(str2))
    str1 = str1.zfill(max_len)
    str2 = str2.zfill(max_len)

    # Perform the XOR operation
    result = int(str1, 16) ^ int(str2, 16)

    # Convert the result back to a hexadecimal string
    result_hex = hex(result)[2:]  # Remove '0x' prefix

    return result_hex

m1 = "LIFEISLIKEABOXOFCHOCOLATES"
c1 = "CXGDXNIPWXYXTONWQTCVCFXKCY"
c2 = "PDVMTQBYWGMSBYZKMAIPWFIXCZ"

# Ensure both strings have the same length
max_len = max(len(m1), len(c1))
m1 = m1.ljust(max_len, '0')  # Pad the shorter string with zeros
c1 = c1.ljust(max_len, '0')

# Compute the OTP key using XOR
otp_key = ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(m1, c1))

max_len = max(len(c2), len(otp_key))
c2 = c2.ljust(max_len, '0')  # Pad the shorter string with zeros
otp_key = otp_key.ljust(max_len, '0')

# Compute m2 by applying the OTP key using XOR
m2 = ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(c2, otp_key))

print(m2)
