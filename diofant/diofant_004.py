#!/usr/bin/env python3

# Палиндром - это такое число, которое читается одинаково слева направо и справа налево, например, 123321.
# Найти наибольший палиндром, который является произведением двух трехзначных чисел.

def is_palindrome(number):
    test_string = str(number)
    length = len(test_string)
    if length % 2 != 0:
        return False
    part1 = test_string[:length//2]
    part2 = test_string[length//2:]
    part2 = part2[::-1]
    if part1 == part2:
        return True
    return False

def main_loop():
    max_value = 0
    for num1 in range(999, 99, -1):
        for num2 in range(num1, 99, -1):
            value = num1 * num2
            if is_palindrome(value):
                if value > max_value:
                    max_value = value
    return max_value

print("Max palindrome: {}".format(main_loop()))
