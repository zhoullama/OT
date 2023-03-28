import random
import gmpy2
# p,q, and h are public numbers.
# p should be a large prime number.
p = 23
g = 5
h = 7

n = 4

if __name__ == '__main__':
    m = [random.SystemRandom().randrange(1, p) for i in range(n)]
    print("m =", m)
    for i in range(12):
        encrypted_m = []
        t = i % 4
        r = random.SystemRandom().randrange(1, p-1)
        y = gmpy2.powmod(g, r, p)
        obfuscator = gmpy2.powmod(h, t, p)
        y = (y * obfuscator) % p
        hi = 1
        for i in range(n):
            k = random.SystemRandom().randrange(1, p - 1)
            a = gmpy2.powmod(g, k, p)
            b = (gmpy2.powmod(y * gmpy2.invert(hi, p), k, p) * m[i]) % p
            hi *= h
            encrypted_m.append((a, b))

        print("encrypted messages:", encrypted_m)
        decrypted_m = [x[1] * gmpy2.invert(gmpy2.powmod(x[0], r, p), p) % p for x in encrypted_m]
        print("decrypted messages:", decrypted_m)
        assert m[t] == decrypted_m[t]
