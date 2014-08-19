#!/usr/bin/env python3
import re
import base64
import binascii

# From RFC 3501
# Valid ASCII chars is 0x20-0x25, 0x27-0x7e.
# Char '&'(0x26) is replaced by two chars '&-'.
# Base64 chars 0x00-0x1f, 0x7f-0xff, ',' replace '/'
# If last char is not ASCII then '-' should be added to end.

utf7_seg = re.compile('&([^-]*)-', re.ASCII)

def decode_base64(matched):
    part = matched.group(1)
    if not part:
        return '&'
    part = part + ('=' * (len(part) % 4))
    return base64.b64decode(part, '+,').decode('utf-16_be')

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: {} FILENAME".format(sys.argv[0]))
        sys.exit(1)
    with open(sys.argv[1], "r") as boxes_list:
        for ln in boxes_list.readlines():
            ln = ln[:-1]
            try:
                print(re.sub(utf7_seg, decode_base64, ln))
            except UnicodeDecodeError as unicode_err:
                print("Line: {}\n  UnicodeError: {}".format(ln, unicode_err))
            except binascii.Error as b64_err:
                print("Line: {}\n  Base64Error: {}".format(ln, b64_err))
