#!/usr/bin/python3.1
# -*- coding: utf-8 -*-
import re
import sys
import cgi
import pickle
import codecs

gr_lmnr=['l','m','n','r']
gr_jqx=['j','q','x']

gr_special={'zhi': ['jy', 'jyr', 'jyy', 'jyh'], \
            'chi': ['chy', 'chyr', 'chyy', 'chyh'], \
            'shi': ['shy', 'shyr', 'shyy', 'shyh'], \
            'ri': ['ry', 'ryr', 'ryy', 'ryh'], \
            'zi': ['tzy', 'tzyr', 'tzyy', 'tzyh'], \
            'ci': ['tsy', 'tsyr', 'tsyy', 'tsyh'], \
            'si': ['sy', 'syr', 'syy', 'syh'], \
            'ju': ['jiu', 'jyu', 'jeu', 'jiuh'], \
            'qu': ['chiu', 'chyu', 'cheu', 'chiuh'], \
            'xu': ['shiu', 'shyu', 'sheu', 'shiuh'], \
            'yi': ['i', 'yi', 'yii', 'yih'], \
            'ya': ['ia', 'ya', 'yea', 'yah'], \
            'yo': ['io', 'yo', 'yeo', 'yoh'], \
            'ye': ['ie', 'ye', 'yee', 'yeh'], \
            'yai': ['iai', 'yai', 'yeai', 'yay'], \
            'yao': ['iau', 'yau', 'yeau', 'yaw'], \
            'you': ['iou', 'you', 'yeou', 'yow'], \
            'yan': ['ian', 'yan', 'yean', 'yann'], \
            'yin': ['in', 'yn', 'yiin', 'yinn'], \
            'yang': ['iang', 'yang', 'yeang', 'yanq'], \
            'ying': ['ing', 'yng', 'yiing', 'yinq'], \
            'yong': ['iong', 'yong', 'yeong', 'yonq'], \
            'wu': ['u', 'wu', 'wuu', 'wuh'], \
            'wa': ['ua', 'wa', 'woa', 'wah'], \
            'wo': ['uo', 'wo', 'woo', 'woh'], \
            'wai': ['uai', 'wai', 'woai', 'way'], \
            'wei': ['uei', 'wei', 'woei', 'wey'], \
            'wan': ['uan', 'wan', 'woan', 'wann'], \
            'wen': ['uen', 'wen', 'woen', 'wenn'], \
            'wang': ['uang', 'wang', 'woang', 'wanq'], \
            'weng': ['ueng', 'weng', 'woeng', 'wenq'], \
            'yu': ['iu', 'yu', 'yeu', 'yuh'], \
            'yue': ['iue', 'yue', 'yeue', 'yueh'], \
            'yuan': ['iuan', 'yuan', 'yeuan', 'yuann'], \
            'yun': ['iun', 'yun', 'yeun', 'yunn'], \
            'r': ['el', 'erl', 'eel', 'ell'], \
            'er': ['el', 'erl', 'eel', 'ell'] \
            }

gr_initial={'b': 'b', 'p': 'p', 'm': 'm', 'f': 'f', \
            'd': 'd', 't': 't', 'n': 'n', 'l': 'l', \
            'g': 'g', 'k': 'k', 'h': 'h', \
            'j': 'j', 'q': 'ch', 'x': 'sh', \
            'r': 'r', 'z': 'tz', 'c': 'ts', 's': 's'\
            }
gr_retroflex={'zh': 'j', 'ch': 'ch', 'sh': 'sh'}

gr_final = {'a': ['a', 'ar', 'aa', 'ah'], \
            'o': ['o', 'or', 'oo', 'oh'], \
            'e': ['e', 'er', 'ee', 'eh'], \
            'ai': ['ai', 'air', 'ae', 'ay'], \
            'ei': ['ei', 'eir', 'eei', 'ey'], \
            'ao': ['au', 'aur', 'ao', 'aw'], \
            'ou': ['ou', 'our', 'oou', 'ow'], \
            'an': ['an', 'arn', 'aan', 'ann'], \
            'en': ['en', 'ern', 'een', 'enn'], \
            'ang': ['ang', 'arng', 'aang', 'anq'], \
            'eng': ['eng', 'erng', 'eeng', 'enq'], \
            'ong': ['ong', 'orng', 'oong', 'onq'], \
            'r': ['l', 'r', 'l', 'l'], \
            'i': ['i', 'yi', 'ii', 'ih'], \
            'ia': ['ia', 'ya', 'ea', 'iah'], \
            'io': ['io', 'yo', 'eo', 'ioh'], \
            'ie': ['ie', 'ye', 'iee', 'ieh'], \
            'iai': ['iai', 'yai', 'eai', 'iay'], \
            'iao': ['iau', 'yau', 'eau', 'iaw'], \
            'iu': ['iou', 'you', 'eou', 'iow'], \
            'ian': ['ian', 'yan', 'ean', 'iann'], \
            'in': ['in', 'yn', 'iin', 'inn'], \
            'iang': ['iang', 'yang', 'eang', 'ianq'], \
            'ing': ['ing', 'yng', 'iing', 'inq'], \
            'iong': ['iong', 'yong', 'eong', 'ionq'], \
            'u': ['u', 'wu', 'uu', 'uh'], \
            'ua': ['ua', 'wa', 'oa', 'uah'], \
            'uo': ['uo', 'wo', 'uoo', 'uoh'], \
            'uai': ['uai', 'wai', 'oai', 'uay'], \
            'ui': ['uei', 'wei', 'oei', 'uey'], \
            'uan': ['uan', 'wan', 'oan', 'uann'], \
            'un': ['uen', 'wen', 'oen', 'uenn'], \
            'uang': ['uang', 'wang', 'oang', 'uanq'], \
            'u:': ['iu', 'yu', 'eu', 'iuh'], \
            'u:e': ['iue', 'yue', 'eue', 'iueh'], \
            'u:an': ['iuan', 'yuan', 'euan', 'iuann'], \
            'u:n': ['iun', 'yun', 'eun', 'iunn'] \
          }

def py2gr(py):
    try:
        err = py
        py = py.lower()
        out = ""
        initial = ""
        tone = int(py[-1])
        py = py[0:-1]
        
        if tone == 5:
            out += "."
            tone = 1
            
        if py in gr_special:
            out += gr_special[py][tone-1]
            return out

        elif py[0:2] in gr_retroflex:
            out += gr_retroflex[py[0:2]]
            py = py[2:]
        elif py[0] in gr_initial:
            initial = py[0]
            out += gr_initial[initial]
            py = py[1:]

        if initial in gr_jqx:
            if py[0] == 'u':
                py = 'u:' + py[1:]

        if initial in gr_lmnr:
            if tone == 1:
                out += "h"
            elif tone == 2:
                tone = 1
        out += gr_final[py][tone-1]
        return out
    except ValueError:
        return ""
    except KeyError:
        return ""

tsyrdict = pickle.load(open('tsyrdict.p', 'rb'))
tsyrdef = pickle.load(open('tsyrdef.p', 'rb'))

ziArr = []
pronArr = []
enArr = []

sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
    
def traverse(inp):
    ziArr[:] = []
    pronArr[:] = []
    enArr[:] = []
    
    start = 0
    #for start in range(len(inp)):
    while start < len(inp):
        chunk = inp[start:start+8]
        for end in range(len(chunk),0,-1):
            parse(chunk[0:end])
            if chunk[0:end] in tsyrdict:
                # end - 1 because cannot avoid line "start += 1"
                start += end - 1
                break
        start += 1
        
def parse(chunk):
    pron = ""
    oldpron = []
    en = ""
    if chunk in tsyrdict:
        # loop through all elements of tsyrdict[chunk]
        for ref in tsyrdict[chunk]:
            line = tsyrdef[ref]
            refpron = re.search('\[(.*?)\]', line).group(1)
            if refpron.lower() not in oldpron:
                pron += refpron + "|"
            oldpron.append(refpron.lower())
            en += "[" + refpron + "] " + re.search('(\/.*\/)', line).group(1)
        pron = pron.rstrip("|")

        # needs fix
        if "|" in pron:
            multpron = pron.split("|")
            for m in range(len(multpron[0].split())):
                combinedpron = ""
                for n in range(len(multpron)):
                    # does not cover A|B|A cases
                    if multpron[n].split()[m] + "|" != combinedpron:
                        combinedpron += multpron[n].split()[m] + "|"
                combinedpron = combinedpron.rstrip("|")
                pronArr.append(combinedpron)
        else:
            pronArr.extend(pron.split())
        ziArr.extend(list(chunk))

        for j in range(len(chunk)):
            enArr.append(en)
        
    else:
        if len(chunk) == 1:
            pronArr.extend(" ")
            enArr.extend(" ")
            ziArr.extend(chunk)

longline = """（中央社記者龍瑞雲台北29日電）台北醫學大學在3月3日至9日針對全台10所大專院校進行「愛情EQ量表」調查，今天發表結果顯示，男女交往過程中最痛苦的是劈腿，新好男人型屬李大仁、新好女人型屬程又青。
台北醫學大學公共衛生學系所副教授呂淑妤表示，「愛情EQ量表」由台北醫學大學研發，針對北、中、南共10所大專院校學生進行問卷調查，共回收問卷2361份，回應率約8成。
調查結果顯示，男女交往的痛苦指數高低程度，最主要是對方或自己劈腿占27.7%，及有第三者介入橫刀奪愛占23.1%、其次是女方懷孕、家長反對及雙方冷戰鬧脾氣占8.1%；當大學生感情遇到困擾時，有24%不願意主動尋求協助，有15%曾涉入三角戀情。
呂淑妤表示，大學生的新好男人條件，是有責任感，溫柔體貼，成熟穩重，就如李大仁型；女大生認為的新好女人應具備獨立自主、善解人意、有智慧的條件，就如程又青型；然而，男大生期待的是溫柔體貼、善解人意、個性好，如女僕店的動漫人物。
調查顯示，男女交往時常見的困擾是溝通不良約65%、個性差異占4成；在戀愛時近8成大學生的戀愛諮詢對象是同學朋友，然而，輔導機構與師長的比率不到2%。
呂淑妤表示，因情傷或處於情感困擾時，不主動求助者較主動求助者有5.5倍的風險會成為自傷族；找不到對方時會連環Call者也容易成為自傷族。
台北醫學大學公衛暨營養學院院長邱弘毅呼籲，青年男女切勿太ㄍㄧㄣ，遇到任何愛情難關，務必要主動求助，避免悲劇發生。呂淑妤也提出預約幸福的三方法，保持距離、勇於表達及共同成長。1010329
（中央社檔案照片"""
#line = "一夜露水Z丁夕K七重要K重L重複"
#line="台"
#line = "abcdefghijk"
#line = "台灣zz大哥大"
form = cgi.FieldStorage()
if "q" in form:
    line = form["q"].value
else:
    line = longline

if "w" in form:
    width = re.findall("([\d.]*\d+)", form["w"].value)[0]
else:
    width = "40"

if int(width) < 20 or int(width) > 60:
  width = "40"

#if line == "":
#    line = "台北醫學大學在恐怖份子"


print("Content-Type: text/html\n\n")

print("""
<!DOCTYPE html>
<html>
<head>
<title>Gwoyeu Romanizer</title>
<meta charset="utf-8">
<style type="text/css">
table { table-layout: fixed; }
td { vertical-align: bottom; }
.col { width:""", end="")
print(width, end="")
print("""px; overflow: hidden; }
.gr { text-align: center; font-size: 12px; font-family: Arial Narrow, Arial, sans-serif; color: #009; }
.hidegr { text-align: center; font-size: 12px; font-family: Arial Narrow, Arial, sans-serif; visibility: hidden; }
.zi { text-align: center; font-size: 24px; }
.hl { background-color: #9cf; }
.attrib { font-size: 12px; font-family: Arial Narrow, Arial, sans-serif; color: #009; }
.pronlink { font-size: 12px; font-family: Arial Narrow, Arial, sans-serif; color: #009; }
</style>
<script type="text/javascript" src="/jquerymin.js"></script>
    <script type="text/javascript">
      $(document).ready(function () {
        $('#togglePron').click(function() {
          $('.gr').toggleClass('hidegr');
        });

        $('#toggleFormBar').click(function() {
          $('#formid').toggle('slow');
        });
      });
    </script>
</head>
<body>
#9
<div id="formid">
<form action="readhash9.py" method="post">
This page marks up (annotates) traditional Chinese characters with the Gwoyeu Romatzyh pronunciation system.<br />
Enter traditional Chinese in the box below.<br />
<textarea name="q" id="textareaQ" cols="80" rows="8">""", end="")

print(line, end="")

print("""</textarea>
<br />
<input type="text" size="4" name="w" value=""", end="")
print('"' + width + '"', end="")
print("""><input type="submit" />
<input type="button" value="Clear" onclick="document.getElementById('textareaQ').value=''" />
</form></div>
<div id="toggleFormBar" style="background-color: #ffee99; width: 100%; padding: 10px;">Hide controls
</div>
<br />
<div class="pronlink" id="togglePron" style="background-color: #9cf; width: 100%; padding: 10px">Show/hide Pronunciation</div>
<br />
<table border="0" cellspacing="0" cellpadding="0">""")

traverse(line)
cols = 20

for ctr in range(len(ziArr)):
    if ctr % cols == 0:
        print('<tr>')

    print('<td nowrap>')
    print('<div class="col" ', end="")
    if len(enArr[ctr]) > 1:
        titlestr = 'title="' + enArr[ctr] + '"'
        print(titlestr, end="")
    print('>')

    pron = pronArr[ctr].split("|")
    if len(pron) > 1:

        altpron = ", ".join(map(py2gr,pron[1:]))
        print('<div class="gr hl" title="' + altpron + '">', end="")
    else:
        print('<div class="gr">', end="")
    print(py2gr(pron[0]), end="")
    print('</div>')

    print('<div class="zi">', end="")
    print(ziArr[ctr]) #.decode('utf-8'))
    print('</div>')
    print('</div>')
    print('</td>\n')

    if ctr % cols == cols - 1:
        print('</tr>')

if ctr % cols != cols - 1:
    print('</tr>')
print('</table>')
print('<br />')
print('<div class="attrib">Uses CC-CEDICT</div>')
print('</body></html>')

#pron = re.search('\[(.*?)\]', line).group(1)
#en = re.search('(\/.*\/)', line).group(1)
