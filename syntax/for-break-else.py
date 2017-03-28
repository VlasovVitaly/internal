#!/usr/bin/env python

def dummy(num):
    pass

print("#1 Else in for loop with break")
for num in range(100):
    if num == 2:
        print("Break")
        break
else:
    print("else")
print()

print("#2 Else in for loop without break")
for num in range(100):
    dummy(num)
else:
    print("else")
print()

print("#3 Else in empty for loop without break")
for num in ():
    print(num)
else:
    print("else")
print()

print("#4 Else in empty for loop with break")
for num in ():
    break
else:
    print("else")
print()
