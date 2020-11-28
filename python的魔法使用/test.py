# -*- coding = utf-8 -*-
# /usr/bin/env python

# @Time    : 20-11-18 下午8:25
# @File    : test.py
# @Software: PyCharm
# try/except/else       while/else  break  continue
# while True:
#     reply = input('Enter txt:')
#     if reply == 'stop':
#         break
#     try:
#         num = int(reply)
#     except:
#         print('Bad!' * 8)
#     else:
#         print(int(reply)**2)
#
# print('Bye')

while True:
    reply = input('Enter txt:')
    if reply == 'stop':
        break
    elif not reply.isdigit():
        print('Bad!'*8)
    else:
        num = int(reply)
        if num < 20:
            print('low'*4)
        else:
            print(num**2)
print('Bye'*3)




