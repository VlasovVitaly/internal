#!/usr/bin/env python3

# Найти наименьшее число, которое делится на все натуральные числа меньшие 25.(2..24)

def gdc(num1, num2):
    while num2 != 0:
        temp = num1 % num2
        num1 = num2
        num2 = temp
    return num1

def lcm(num1, num2):
    return (num1 * num2) // gdc(num1, num2)

prev = 2
for num in range(3, 25, 1):
    prev = lcm(prev, num)

print("Final: {}".format(prev))
