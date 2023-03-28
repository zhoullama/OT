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


def RSADecrypt(ciphertext, secret_key):
    n = secret_key[1]
    d = secret_key[0]
    return gmpy2.powmod(ciphertext, d, n)


if __name__ == '__main__':
    # The sender generates two pairs of public-secret keys.
    pk1, pk2, sk1, sk2 = RSAKeypair.generate_keypairs()
    print("pk1 =", pk1)
    print("pk2 =", pk2)
    print("sk1 =", sk1)
    print("sk2 =", sk2)
    n = pk1[1]
    print("n =", n)

    '''RSA encryption and decryption tests
    message = gmpy2.mpz(1234567890)
    print("Plaintext message:", message)
    encrypted_message = RSAEncrypt(message, pk1)
    print("Encrypted message:", encrypted_message)
    decrypted_message = RSADecrypt(encrypted_message, sk1)
    print("Decrypted message:", decrypted_message)
    assert message == decrypted_message
    '''

    m1 = bytes('I love you.', 'utf-8')
    m2 = bytes('Hello, world!', 'utf-8')
    m1_len = len(m1)
    m2_len = len(m2)
    m1 = int.from_bytes(m1, 'little')
    m2 = int.from_bytes(m2, 'little')
    assert m1 < n and m2 < n
    # print("m1:", m1)
    # print("m2:", m2)

    # 1-out-of-2 OT simulation
    # The receiver generates a random number k and transfers it to the sender.
    for i in range(10):
        k = random.SystemRandom().randrange(1, n)
        pk = pk1 if i % 2 == 1 else pk2
        encrypted_k = RSAEncrypt(k, pk)

    # The sender decrypts k using both sk1 and sk2.
        k1 = RSADecrypt(encrypted_k, sk1)
        k2 = RSADecrypt(encrypted_k, sk2)
    # Then transfer two masked messages back to the sender.
        masked_m1 = m1 ^ k1
        masked_m2 = m2 ^ k2

    # The receiver remains oblivious as to what piece has been transferred.
        derived_m1 = masked_m1 ^ k
        derived_m2 = masked_m2 ^ k
        print("derived_m1:", derived_m1)
        print("derived_m2:", derived_m2)
        if i % 2 == 1:
            print(int.to_bytes(int(derived_m1), m1_len, 'little').decode('utf-8'))
        else:
            print(int.to_bytes(int(derived_m2), m2_len, 'little').decode('utf-8'))

