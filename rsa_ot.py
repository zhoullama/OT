import random
import gmpy2
import gmpy_math

class RSAKeypair(object):
    def __init__(self):
        pass

    @staticmethod
    def generate_keypairs(n_length=1024):
        p = q = n = None
        n_len = 0
        while n_len != n_length:
            p = gmpy_math.getprimeover(n_length // 2)
            q = p
            while q == p:
                q = gmpy_math.getprimeover(n_length // 2)
            n = p * q
            n_len = n.bit_length()
        phi_n = (p-1) * (q-1)

        e1 = random.SystemRandom().randrange(3, phi_n)
        while gmpy2.gcd(e1, phi_n) != 1:
            e1 = random.SystemRandom().randrange(3, phi_n)

        e2 = random.SystemRandom().randrange(3, phi_n)
        while e2 == e1 or gmpy2.gcd(e2, phi_n) != 1:
            e2 = random.SystemRandom().randrange(3, phi_n)

        d1 = gmpy2.invert(e1, phi_n)
        d2 = gmpy2.invert(e2, phi_n)

        pk1 = (e1, n)
        pk2 = (e2, n)
        sk1 = (d1, n)
        sk2 = (d2, n)

        return pk1, pk2, sk1, sk2


def RSAEncrypt(plaintext, public_key):
    n = public_key[1]
    e = public_key[0]
    return gmpy2.powmod(plaintext, e, n)


def RSADecrypt(ciphertext, private_key):
    n = private_key[1]
    d = private_key[0]
    return gmpy2.powmod(ciphertext, d, n)


if __name__ == '__main__':
    pk1, pk2, sk1, sk2 = RSAKeypair.generate_keypairs()
    print("pk1 =", pk1)
    print("pk2 =", pk2)
    print("sk1 =", sk1)
    print("sk2 =", sk2)
    message = gmpy2.mpz(1234567890)
    print("Plaintext message:", message)
    encrypted_message = RSAEncrypt(message, pk1)
    print("Encrypted message:", encrypted_message)
    decrypted_message = RSADecrypt(encrypted_message, sk1)
    print("Decrypted message:", decrypted_message)
    assert message == decrypted_message
