# From https://eli.thegreenplace.net/2019/rsa-theory-and-implementation/

from utils import *

def generate_rsa_key(p, q):
    n = p * q
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
        print("\t\tWarning: Message is too big for RSA key")
    return (data ** key['exp']) % key['mod']

if __name__ == "__main__":
    keys = generate_rsa_key(449, 313)
    print("Generated RSA Keys:")
    print(keys)

    while True:
        m = input("Enter message: ")
        encoded_m = string_to_int(m)
        if encoded_m > keys['public']['mod']:
            print("Message too long for RSA key, please enter shorter message")
        else:
            break

    print(f"Encoded message: {string_to_int(m)}")
    print()

    print("Encrypting with private key...")
    c = crypt(encoded_m, keys['private'])
    print(f"Ciphertext: {c}")
    print("Decrypting with public key...")
    print(f"Decrypted encoded message: {crypt(c, keys['public'])}")
    print(f"Decrypted message: {int_to_string(crypt(c, keys['public']))}")
    print()

    print("Encrypting with public key...")
    c = crypt(encoded_m, keys['public'])
    print(f"Ciphertext: {c}")
    print("Decrypting with private key...")
    print(f"Decrypted encoded message: {crypt(c, keys['private'])}")
    print(f"Decrypted message: {int_to_string(crypt(c, keys['private']))}")
