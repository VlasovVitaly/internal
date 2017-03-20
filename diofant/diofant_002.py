#!/usr/bin/env python3

# Имеется ряд чисел Фибоначчи: 1, 1, 2, 3, 5, 8, 13, 21,...
# (каждый следующий член ряда равен сумме двух предыдущих, начинается ряд с двух единиц).
# Найти сумму членов этого ряда, меньших одного миллиарда и находящихся на нечетных позициях.
# Внимание! Ответом на задачу является целое число в десятичной записи без пробелов.

value = 1
prev_value = 0
cur_position = 1
total = 0

def next_num(position, number, prev_number):
    return (number + prev_number, number)

while(value < 1000000000):
    if cur_position % 2 != 0:
        total = total + value
    value, prev_value = next_num(cur_position, value, prev_value)
    cur_position = cur_position + 1

print("Total: {}".format(total))
