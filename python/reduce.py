#!/usr/bin/python3.1

import random
import cgi

print("""content-type: text/html

<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="fr" xml:lang="fr"
<body>
""")

form = cgi.FieldStorage()
raw = form.getvalue('j')
# sanitize raw string, allowing only numbers and commas
jcsv = raw

jobs = jcsv.split(',')
if len(jobs) == 1:
    print("ZOMG " + str(jobs) + " iz ur dreem jobz!!1")
else:
    print(str(jobs) + "<br>")
    index1 = 0
    index2 = 0
    while(index1 == index2):
        index1 = random.randint(0, len(jobs)-1)
        index2 = random.randint(0, len(jobs)-1)

    print("<br><br>")
    print(jobs[index1])
    newjobs1 = jobs[:]
    newjobs1.remove(newjobs1[index2])
    print(str(newjobs1))
    print('<br><br><a href="reduce.py?j=' + ",".join(newjobs1) + '">next round</a>')
    
    print("<br><br>")
    print(jobs[index2])
    newjobs2 = jobs[:]
    newjobs2.remove(newjobs2[index1])
    print(str(newjobs2))
    print('<br><br><a href="reduce.py?j=' + ",".join(newjobs2) + '">next round</a>')



print("</body></html>")
