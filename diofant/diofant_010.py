#/usr/bin/env python3

# Чему равна сумма простых чисел меньших 3 миллионов?

import time

max_num = 3000000
def PrimesSieve(num):
    primes = set()
    multiples = set()

    for i in range(2, num +1):
        if i not in multiples:
            primes.add(i)
        multiples.update(range(i*i, num + 1, i))
    return primes

start = time.time()
summ = sum(PrimesSieve(max_num))

elapsed = (time.time() - start)
print("Nubmer: {}, Time: {} seconds".format(summ, elapsed))
