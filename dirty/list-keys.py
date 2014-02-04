#!/usr/bin/env python3

import curses

keys = []
max_len = 0

def add_key(string, num):
    keys.append((string, num))
    global max_len
    if len(string) > max_len:
        max_len = len(string)

add_key('Escape', 27)
add_key('\\n', 10)
add_key('KEY_UP', curses.KEY_UP)
add_key('KEY_DOWN', curses.KEY_DOWN)
add_key('KEY_NPAGE', curses.KEY_NPAGE)
add_key('KEY_PPAGE', curses.KEY_PPAGE)
add_key('KEY_RIGHT', curses.KEY_RIGHT)
add_key('KEY_LEFT', curses.KEY_LEFT)
add_key('CTRL + U', 0x15)
add_key('KEY_BACKSPACE', curses.KEY_BACKSPACE)
add_key('OTHER BACKSPACE', 127)
add_key('KEY_F2', curses.KEY_F2)
add_key('CURSES ERR', curses.ERR)

max_len = max_len + 2
# Header
print("\u250C{}\u252C{}\u252C{}\u252C{}\u2510".
format('\u2500' * max_len, '\u2500' * 9, '\u2500' * 8, '\u2500' * 18))
print("\u2502{:^{key_len}}\u2502{:^9}\u2502{:^8}\u2502{:^18}\u2502".
      format("Key", "Decimal", "HEX", "Binary", key_len=max_len))
# Items
#for item in keys:
for item in sorted(keys, key=lambda k: k[1], reverse=True):
    s, i = item[0], item[1]
    print("\u251C{}\u253C{}\u253C{}\u253C{}\u2524".
    format('\u2500' * max_len, '\u2500' * 9, '\u2500' * 8, '\u2500' * 18))
    print("\u2502{:<{key_len}}\u2502{:9}\u2502 0x{:04X} \u2502 {:016b} \u2502".
    format(s, i, i, i, key_len=max_len))
# end line
print("\u2514{}\u2534{}\u2534{}\u2534{}\u2518".
format('\u2500' * max_len, '\u2500' * 9, '\u2500' * 8, '\u2500' * 18))
