import math

def get_prime_factors(n):
    prime_factors = set([])
    for i in reversed(range(2, int(n/2) + 1)):
        if n % i == 0:
            prime_factors = prime_factors.union(
                get_prime_factors(i))

    return prime_factors if len(prime_factors) > 0 else set([n])

def get_smaller_odd_coprime(n):
    if n <= 3 or not isinstance(n, int):
        raise ValueError("Need integer greater than 2")

    prime_factors = get_prime_factors(n)
    for i in range(3, n):
        if i % 2 == 1 and len(get_prime_factors(i).intersection(prime_factors)) == 0:
            return i

    return None

def get_modular_multiplicative_inverse(n, modulus):
    # Could implement Extended Euclidean Algorithm to speed up
    # quite a bit
    if len(get_prime_factors(n).intersection(get_prime_factors(modulus))) > 0:
        return None

    i = 1
    while True:
        if (n * i - 1) % modulus == 0:
            return i
        i += 1

CHUNK_SIZES = {
    'ascii' : 1,
    'utf-8' : 4
}
ENCODING = 'ascii'
CHUNK_SIZE = CHUNK_SIZES['ascii']

# From https://stackoverflow.com/questions/69801359
# /python-how-to-convert-a-string-to-an-integer-for-rsa-encryption
def string_to_int(s):
    return int.from_bytes(s.encode(ENCODING), byteorder='little')

def int_to_string(i):
    length = math.ceil(i.bit_length() / 8)
    return i.to_bytes(length, byteorder='little').decode(ENCODING)

if __name__ == '__main__':
    m = input("Enter message: ")

    m_int = string_to_int(m)
    print(m_int)
    print(int_to_string(m_int))
