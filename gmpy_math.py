import random
import gmpy2


def getprimeover(n_length):
    r = gmpy2.mpz(random.SystemRandom().getrandbits(n_length))
    r = gmpy2.bit_set(r, n_length-1)
    return gmpy2.next_prime(r)


if __name__ == '__main__':
    n_list = [2 ** x for x in range(1, 11)]
    for n in n_list:
        print("n =", n)
        t_min = 2**(n-1)
        for i in range(10):
            t = getprimeover(n)
            print("t =", t)
            assert t >= t_min
