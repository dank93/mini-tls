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

    # Online literature says this value is conventional for
    # computational efficiency, though I haven't looked into
    # why
    if n > 65537: return 65537

    prime_factors = get_prime_factors(n)
    for i in range(3, n):
        if i % 2 == 1 and len(get_prime_factors(i).intersection(prime_factors)) == 0:
            return i

    return None

def get_modular_multiplicative_inverse(n, modulus):
    # Extended Eucliden Aglorithm, taken from
    # https://en.wikibooks.org/wiki/Algorithm_Implementation/
    # Mathematics/Extended_Euclidean_algorithm
    a = n
    b = modulus
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        (q, a), b = divmod(b, a), a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return x0

CHUNK_SIZES = {
    'ascii' : 1,
    'utf-8' : 4
}

# From https://stackoverflow.com/questions/69801359
# /python-how-to-convert-a-string-to-an-integer-for-rsa-encryption
def string_to_int(s, encoding='utf-8'):
    return int.from_bytes(s.encode(encoding), byteorder='little')

def int_to_string(i, encoding='utf-8'):
    length = math.ceil(i.bit_length() / 8)
    return i.to_bytes(length, byteorder='little').decode(encoding)

if __name__ == '__main__':
    m = input("Enter message: ")

    m_int = string_to_int(m, 'utf-8')
    print(m_int)
    print(int_to_string(m_int, 'utf-8'))

