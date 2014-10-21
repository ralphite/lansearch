# -*- coding: UTF-8 -*-

import os
import os.path
from datetime import datetime

root = ur'\\corp\china\Public Folders'
#root = ur'e:\personal'
f = open('f.txt', 'w')

for r, ds, fs in os.walk(root):
    for n in fs:
        f.write((os.path.join(r, n) + os.linesep).encode('utf-8'))

f.flush()
f.close()

f1 = open('f1.txt', 'w')

for line in open('f.txt', 'r'):
    try:
        line = line.strip()
        size = os.path.getsize(line.decode('utf-8'))
        mtime = os.path.getmtime(line.decode('utf-8'))
        f1.write(
            ('"' + line.decode('utf-8') + '","' + str(size) + '","'
             + str(mtime) + '"' + os.linesep).encode('utf-8')
        )
    except Exception, e:
        print e

f1.flush()
f1.close()