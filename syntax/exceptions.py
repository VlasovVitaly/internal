#!/usr/bin/evn python


print('#1 Exceptuion class inheritance order')
try:
    int(list())
except TypeError as terr:
    print('Raised TypeError')
except Exception as err:
    print('Raised Exception')
print()
