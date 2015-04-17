#!/usr/bin/env python
import re
import os
import codecs
import sys

subre = re.compile(r'(\w+): 0,(\d+:\d{2}:\d{2})\.\d+,.+,\d+,,(?:\{\\[^\}]+\})?([^\r\n]+)\r?\n', re.U)

def readLines(fpath):
    try:
        return codecs.open(fpath, 'r', "utf-8").readlines()
    except UnicodeDecodeError:
        try:
            return codecs.open(fpath, 'r', "utf-16").readlines()
        except UnicodeDecodeError:
            print "Could not determine encoding of file: "+fpath
            return

def convertFile(fpath):
    lines = readLines(fpath)
    if (lines):
        outpath = fpath+".txt"
        with codecs.open(outpath, "w", "utf-8") as outf:
            lastLine = None
            for line in lines:
                m = subre.match(line)
                if (m):
                    if (m.group(1) == "Dialogue" and len(m.group(3)) > 0):
                        cleanedLine = subre.sub(r'\2 \3\n', line)
                        cleanedLine = re.sub(r'\\N', '', cleanedLine)
                        cleanedLine = re.sub(r'\{\\[^\}]+?\}', '', cleanedLine)
                        cleanedLine = re.sub(r'  +', ' -- ', cleanedLine)
                        if (lastLine != cleanedLine):
                          outf.write(cleanedLine)
                          lastLine = cleanedLine
                    else:
                        print "Non-dialogue match (not yet supported): "+m.group(1)
            print "Success: "+outpath

for arg in sys.argv[1:]:
    if (os.path.isfile(arg)):
        if (arg.endswith(".ass")):
          convertFile(arg)
        else:
          print "Skipping (non .ass): "+arg
    else:
        print "File does not exist: "+arg
