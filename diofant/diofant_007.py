#!/usr/bin/env python3

# Имеется ряд простых чисел, идущих подряд: 2, 3, 5, 7, 11,... Какое число находится на позиции 100001.

import time

def is_prime(num):
    if num <= 3:
        if num <= 1:
            return False
        return True
    if not num % 2 or not num % 3:
        return False
    for i in range(5, int(num ** 0.5) + 1, 6):
        if not num % i or not num % (i + 2):
            return False
    return True

def get_nprime(index):
    index = index - 1
    to_check = 3
    while index != 0:
        if is_prime(to_check):
            index = index - 1
        to_check = to_check + 2
    else:
        return to_check - 2

start = time.time()
prime = get_nprime(100001)
elapsed = (time.time() - start)

print("Nubmer: {}, Time: {} seconds".format(prime, elapsed))
