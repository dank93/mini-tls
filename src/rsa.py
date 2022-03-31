# From https://eli.thegreenplace.net/2019/rsa-theory-and-implementation/

from utils import *

ENCODING = 'utf-8'
CHUNK_SIZE = CHUNK_SIZES[ENCODING]

def _max_encryptable_bytes(mod):
    # Every 3 digits in the decimal mod can encrypt one byte
    # so div by 3. Then subtract 1 to handle encoded messages
    # that have the same number of digits as the modulus but
    # are larger (e.g. message=324 wraps a mod of 211).
    return int(len(str(mod)) / 3 - 1)

def generate_rsa_key(p, q):
    n = p * q

    meb = _max_encryptable_bytes(n)
    reqd_chunk_size = CHUNK_SIZES[ENCODING]
    if (meb < reqd_chunk_size):
        raise ValueError(f"RSA key gen inputs too small to encode utf-8" +
                         f" (can encrypt {meb} bytes, " +
                         f"need {reqd_chunk_size}, n={n}). Alternatively, try" +
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

def _crypt(data, key):
    if data > key['mod']:
        raise ValueError("\t\tWarning: Message is too big for RSA key")

    # Given a modulus z, python builtin pow() uses fast modular
    # exponentiation
    return pow(data, key['exp'], key['mod'])

def rsa_encrypt(string_data, key):
    encoded = string_data.encode(ENCODING)
    meb = _max_encryptable_bytes(key['mod'])
    chunked = [encoded[i:i+meb] for i in range(0, len(encoded), meb)]
    return [_crypt(int.from_bytes(c, byteorder='little'), key) for c in chunked]

def rsa_decrypt(cipher_iter, key):
    out = ''
    for c in cipher_iter:
        out += int_to_string(_crypt(c, key), ENCODING)
    return out

if __name__ == "__main__":
    # 2048-bit primes taken from https://stackoverflow.com/questions/22079315/i-need-2048bit-primes-in-order-to-test-the-upper-limits-of-my-rsa-program
    keys = generate_rsa_key(
	32317006071311007300714876688669951960444102669715484032130345427524655138867890893197201411522913463688717960921898019494119559150490921095088152386448283120630877367300996091750197750389652106796057638384067568276792218642619756161838094338476170470581645852036305042887575891541065808607552399123930385521914333389668342420684974786564569494856176035326322058077805659331026192708460314150258592864177116725943603718461857357598351152301645904403697613233287231227125684710820209725157101726931323469678542580656697935045997268352998638215525166389647960126939249806625440700685819469589938384356951833568218188663,
	32317006071311007300714876688669951960444102669715484032130345427524655138867890893197201411522913463688717960921898019494119559150490921095088152386448283120630877367300996091750197750389652106796057638384067568276792218642619756161838094338476170470581645852036305042887575891541065808607552399123930385521914333389668342420684974786564569494856176035326322058077805659331026192708460314150258592864177116725943603718461857357598351152334063994785580370721665417662212881203104945914551140008147396357886767669820042828793708588252247031092071155540224751031064253209884099238184688246467489498721336450133889385773
    )

    print("Generated RSA Keys:")
    print(keys)
    print()

    m = input("Enter message: ")
    print()

    print("Encrypting with private key...")
    c = rsa_encrypt(m, keys['private'])
    print(f"Ciphertext: {c}")
    print("Decrypting with public key...")
    print(f"Decrypted message: {rsa_decrypt(c, keys['public'])}")
    print()

    print("Encrypting with public key...")
    c = rsa_encrypt(m, keys['public'])
    print(f"Ciphertext: {c}")
    print("Decrypting with private key...")
    print(f"Decrypted message: {rsa_decrypt(c, keys['private'])}")

