#!/usr/bin/env python3

# Найти наибольший простой делитель числа 386745374779148463746059.

number = 386745374779148463746059

def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    return not any(num % x == 0 for x in range(3, int(num**0.5) + 1, 2))

while(True):
    for i in range(2, number):
        if is_prime(i):
            if number % i == 0:
                number = number // i
                break
    else:
        break

print("Found: {}".format(number))
