#!/usr/bin/env python3

# Найти разность (1+2+3... +200)^2 - (1^2+2^2+3^2+...+200^2).

def triangular_num(num):
    return (num * (num + 1)) // 2

def square_summ(num):
    summ = 0
    for i in range(1, num + 1, 1):
        summ = summ + (i ** 2)
    return summ

part1 = triangular_num(200) ** 2
part2 = square_summ(200)

print("Result: {}".format(part1 - part2))
