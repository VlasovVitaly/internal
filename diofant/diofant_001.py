#!/usr/bin/env python3

# Найти сумму всех натуральных чисел меньших 1000,
# каждое из которых не делится ни на 3, ни на 5, ни на 7.

def check_num(num):
    for i in (3, 5, 7):
        if num % i == 0:
            return False
    return True

total = 0
for number in range(1, 1000):
    if check_num(number):
        total = total + number

print("Total: {}".format(total))
