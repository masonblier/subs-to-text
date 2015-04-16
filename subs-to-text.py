#!/usr/bin/env python
import re
import os
import sys

subre = re.compile(r'(\w+): 0,(\d+:\d{2}:\d{2})\.\d+,.+,\d+,,(?:\{\\.+\})?([^\r]+)\r?\n')

def convertFile(fpath):
    with open(fpath, "r") as inf:
        with open(fpath+".txt", "w") as outf:
            lastLine = None
            for line in inf:
                m = subre.match(line)
                if (m):
                    if (m.group(1) == "Dialogue" and len(m.group(3)) > 0):
                        cleanedLine = subre.sub(r'\2 \3\n', line)
                        cleanedLine = re.sub(r'\\N', '', cleanedLine)
                        cleanedLine = re.sub(r'\{\\.+?\}', '', cleanedLine)
                        cleanedLine = re.sub(r'  +', ' -- ', cleanedLine)
                        if (lastLine != cleanedLine):
                          outf.write(cleanedLine)
                          lastLine = cleanedLine
                    else:
                        print "Non-dialogue match: "+m.group(1)

for arg in sys.argv[1:]:
    if (os.path.isfile(arg)):
        if (arg.endswith(".ass")):
          convertFile(arg)
        else:
          print "Skipping (non .ass): "+arg
    else:
        print "File does not exist: "+arg
