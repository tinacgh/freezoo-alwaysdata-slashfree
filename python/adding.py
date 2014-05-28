#!/usr/bin/python3.1
import sys, os, codecs, cgi

sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
print("Content-Type: text/html\n\n")

print("""<!DOCTYPE html>
<html><head><meta charset="utf-8"></head>
<body>
""")

print(1+1)
