__author__ = 'yawen'

'''
crawl lan and generate csv results

files.csv
machine, path, file name, file size, mtime, added, deleted
chn-yawen, shared, /path/to/file/, hello.txt, 10, 10/12/2014 23:09:01, true, false
'''

'''
parse from find . -type f -print0|xargs -0 ls -l>files.txt
'''

from os.path import basename, dirname

fw = open('files.csv', 'a')

for line in open('files.txt'):
    line = line.strip()
    line = line[33:]
    line = line.strip()
    ls = line.split(' ', 1)
    machine = 'chn-yawen'
    path = dirname(ls[1][13:])
    file_name = basename(ls[1][13:])
    size = ls[0]
    mtime = ls[1][:12]
    added = 'false'
    deleted = 'false'
    res = '"' + '","'.join((machine, path, file_name, size, mtime, added, deleted)) + '"'
    fw.write("\n" + res)

fw.flush()
fw.close()