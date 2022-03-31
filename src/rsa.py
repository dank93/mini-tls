# From https://eli.thegreenplace.net/2019/rsa-theory-and-implementation/

from utils import *

ENCODING = 'ascii'
CHUNK_SIZE = CHUNK_SIZES[ENCODING]

def generate_rsa_key(p, q):
    n = p * q

    # Every 3 digits in the decimal mod can encrypt one byte
    # so div by 3. The subtract 1 to handle encoded messages
    # That have the same number of digits as the modulus but
    # are larger (e.g. message=324 wraps a mod of 211).
    max_encryptable_bytes = int(len(str(n)) / 3 - 1)

    if (max_encryptable_bytes < CHUNK_SIZE):
        raise ValueError(f"RSA key gen inputs too small to encode utf-8" +
                         f" (can encrypt {max_encryptable_bytes} bytes, " +
                         f"need {CHUNK_SIZE}, n={n}). Alternatively, try" +
                         f" ascii encoding")

    phi = (p - 1) * (q - 1)
    e = get_smaller_odd_coprime(phi)
    d = get_modular_multiplicative_inverse(e, phi)

    return {
        'p' : p,
        'q' : q,
        'phi' : phi,
        'public' : {'exp' : e, 'mod' : n},
        'private' : {'exp' : d, 'mod' : n},
    }

def crypt(data, key):
    if data > key['mod']:
        raise ValueError("\t\tWarning: Message is too big for RSA key")

    # Given a modulus z, python builtin pow() uses fast modular
    # exponentiation
    return pow(data, key['exp'], key['mod'])

def encrypt(string_data, key):
    encoded = string_data.encode(ENCODING)
    chunked = [encoded[i:i+CHUNK_SIZE] \
               for i in range(0, len(encoded), CHUNK_SIZE)]
    return [crypt(int.from_bytes(c, byteorder='little'), key) for c in chunked]

def decrypt(cipher_iter, key):
    out = ''
    for c in cipher_iter:
        out += int_to_string(crypt(c, key), ENCODING)
    return out

if __name__ == "__main__":
    keys = generate_rsa_key(449, 313)
    print("Generated RSA Keys:")
    print(keys)
    print()

    m = input("Enter message: ")
    print()

    print("Encrypting with private key...")
    c = encrypt(m, keys['private'])
    print(f"Ciphertext: {c}")
    print("Decrypting with public key...")
    print(f"Decrypted message: {decrypt(c, keys['public'])}")
    print()

    print("Encrypting with public key...")
    c = encrypt(m, keys['public'])
    print(f"Ciphertext: {c}")
    print("Decrypting with private key...")
    print(f"Decrypted message: {decrypt(c, keys['private'])}")

