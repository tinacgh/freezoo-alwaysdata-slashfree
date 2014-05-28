#!/usr/bin/python3.1

import sys
import codecs

f = codecs.open(sys.stdout, "w", "utf-8")

mystr = "你好世界"
f.write("Content-Type: text/html\n\n")

f.write("""<!DOCTYPE html>
<html><head><meta charset="utf-8"></head>
<body>
""")

f.write(mystr)
