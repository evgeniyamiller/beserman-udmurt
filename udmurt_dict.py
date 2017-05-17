import re, json

def openfile(name):
    f = open(name, 'r', encoding = 'utf-8')
    text = f.readlines()
    f.close()
    return text

def makedict(text):
    A = []
    for line in text:
        if 'lex:' in line:
            a = []
            a.append(line[6:].replace('\n',''))
        elif 'gramm:' in line:
            a.append(line[8:].replace('\n',''))
        elif 'trans_ru:' in line:
            a.append(line[11:].replace('\n',''))
            A.append(a)
    return A

def writefile(name, text):
    fw = open(name, 'w', encoding = 'utf-8')
    fw.write(text) 
    fw.close()


#string = ''
#row = '%s\t%s\t%s\n'
#for i in ['udm_lexemes_ADJ.txt', 'udm_lexemes_IMIT.txt', 'udm_lexemes_N.txt', 'udm_lexemes_N_persn.txt', 'udm_lexemes_NRel.txt', 'udm_lexemes_PRO.txt', 'udm_lexemes_unchangeable.txt', 'udm_lexemes_V.txt']:
 #   A = makedict(openfile(i))
 #   for el in A:
  #      string += row % (el[0], el[1], el[2])
   # writefile('udmlex.tsv', string)

#alf = 'абвгдежзийклмнопрстуфхцчшыьёюяӧӝӟӵ'
#trans = list('abvgdežzijklmnoprstufxcčšə')
#trans.append('ə̂')
#trans.append('ə̈əɤ')

dic2cyr = {'a': 'а', 'b': 'б', 'v': 'в',
           'g': 'г', 'd': 'д', 'e': 'э',
           'ž': 'ж', 'š': 'ш', 'ɤ': 'ӧ',
           'ə': 'ө', 'ǯ': 'ӟ', 'č': 'ч',
           'z': 'з', 'i': 'ӥ', 'j': 'й', 'k': 'к',
           'l': 'л', 'm': 'м', 'n': 'н',
           'o': 'о', 'p': 'п', 'r': 'р',
           's': 'с', 't': 'т', 'u': 'у',
           'c': 'ц', 'w': 'у', 'x': 'х',
           'y': 'ы', 'f': 'ф', 'ɨ': 'ы'}
cyr2dic = {'а': 'a', 'б': 'b', 'в': 'v',
           'г': 'g', 'д': 'd', 'э': 'e',
           'ж': 'ž', 'ш': 'š', 'ӧ': 'ӧ',
           'ӟ': 'ǯʼ', 'ӝ': 'ǯ', 'ч': 'č',
           'з': 'z', 'ӥ': 'i', 'й': 'j', 'к': 'k',
           'л': 'l', 'м': 'm', 'н': 'n',
           'о': 'o', 'п': 'p', 'р': 'r',
           'с': 's', 'т': 't', 'у': 'u',
           'ц': 'c', 'x': 'х', 'ф': 'f',
           'ӵ': 'č', 'ч': 'čʼ', 'щ': 'šʼ',
           'я': 'ʼa', 'е': 'ʼe', 'и': 'ʼi',
           'ё': 'ʼo', 'ю': 'ʼu', 'ь': 'ʼ', 'ы': 'ə'}
cyrHard2Soft = {'а': 'я', 'э': 'е', 'ӥ': 'и', 'о': 'ё', 'у': 'ю'}
rxSoften = re.compile('(?<![чӟ])ʼ([аэӥоу])', flags=re.U)
rxCyrSoften = re.compile('([čǯ])(?!ʼ)', flags=re.U)
rxCyrMultSoften = re.compile('ʼ{2,}', flags=re.U)
rxNeutral1 = re.compile('(?<=[бвгжкмпрфхцчшщйʼ])([эӥ])', flags=re.U)
rxNeutral2 = re.compile('([бвгжкмпрфхцчʼаоэӥуяёеию]|\\b)(ӥ)', flags=re.U)
rxCyrNeutral = re.compile('(?<=[bvgzkmprfxcwj])ʼ', flags=re.U)
rxCJV = re.compile('(?<=[бвгджзӟклмнпрстфхцчшщ])й([аэӥоу])', flags=re.U)
rxSh = re.compile('ш(?=[ʼяёюие])', flags=re.U)
rxZh = re.compile('ж(?=[ʼяёюие])', flags=re.U)
rxVJV = re.compile('(?<=[аеёиӥоӧөуыэюяʼ])й([аэоу])', flags=re.U)
rxJV = re.compile('\\bй([аэоу])', flags=re.U)
rxCyrVJV = re.compile('([aeiouɨəɤӧ])ʼ([aeouɨəɤ])', flags=re.U)
rxCyrVSoft = re.compile('([aeiouɨəɤ]|\\b)ʼ', flags=re.U)
rxCyrJV = re.compile('\\bʼ([aeouɨəɤ])', flags=re.U)
rxExtraSoft = re.compile('([дзлнст])ь\\1(?=[ьяеёию])', flags=re.U)
rxCyrExtraSoft = re.compile('([džlnšt])\\1(?=ʼ)', flags=re.U)
rxCyrW = re.compile('(\\b|[кр])у(?=[аоэи])', flags=re.U)

def convert_output(res, trans):
    if trans == 'ural':
        res = res.replace('ə', 'ə̑')
        res = res.replace('ɤ', 'e̮')
        res = res.replace('ɨ', 'i̮')
        res = res.replace('čʼ', 'č')
        res = res.replace('ǯʼ', 'ǯ')
        res = res.replace('šʼ', 'sʼ')
        res = res.replace('žʼ', 'zʼ')

    if trans == 'corpus':
        res = res.replace('ə', 'ə̑')
        res = res.replace('ɤ', 'ə')
        res = res.replace('ɨ', 'y')
        res = res.replace('ʼ', '’')

    if trans == 'cyr':
        letters = []
        for letter in res:
            try:
                letters.append(dic2cyr[letter.lower()])
            except KeyError:
                letters.append(letter)
        res = ''.join(letters)
        res = rxSoften.sub(lambda m: cyrHard2Soft[m.group(1)], res)
        res = rxSh.sub('с', res)
        res = rxZh.sub('з', res)
        res = rxVJV.sub(lambda m: cyrHard2Soft[m.group(1)], res)
        res = rxVJV.sub(lambda m: cyrHard2Soft[m.group(1)], res)
        res = rxJV.sub(lambda m: cyrHard2Soft[m.group(1)], res)
        res = rxNeutral1.sub(lambda m: cyrHard2Soft[m.group(1)], res)
        res = rxNeutral2.sub('\\1и', res)
        res = rxCJV.sub(lambda m: 'ъ' + cyrHard2Soft[m.group(1)], res)
        res = res.replace('ӟʼ', 'ӟ')
        res = res.replace('чʼ', 'ч')
        res = res.replace('ʼ', 'ь')
        res = rxExtraSoft.sub('\\1\\1', res)

    return res


def convert_input(req, trans):
    if trans == 'ural':
        req = req.replace('ə̑', 'ə')
        req = req.replace('e̮', 'ɤ')
        req = req.replace('i̮', 'ɨ')
        req = req.replace('č', 'čʼ')
        req = req.replace('ǯ', 'ǯʼ')
        req = req.replace('sʼ', 'šʼ')
        req = req.replace('zʼ', 'žʼ')

    if trans == 'corpus':
        req = re.sub('ə(?!̑)', 'ɤ', req)
        req = req.replace('ə̑', 'ə')
        req = req.replace('y', 'ɨ')
        req = req.replace('’', 'ʼ')

    if trans == 'cyr':
        #req = rxCyrW.sub('\\1w', req)
        req = req.replace('жи', 'жӥ')
        req = req.replace('ши', 'шӥ')
        req = req.replace('же', 'жэ')
        req = req.replace('ше', 'шэ')
        letters = []
        for letter in req:
            try:
                letters.append(cyr2dic[letter.lower()])
            except KeyError:
                letters.append(letter)
        req = ''.join(letters)
        req = rxCyrVJV.sub('\\1j\\2', req)
        req = rxCyrJV.sub('j\\1', req)
        req = req.replace('ъʼ', 'j')
        req = req.replace('sʼ', 'šʼ')
        req = req.replace('zʼ', 'žʼ')
        #req = rxCyrSoften.sub('\\1ʼ', req)
        req = rxCyrNeutral.sub('', req)
        req = rxCyrExtraSoft.sub('\\1ʼ\\1', req)
        req = req.replace('sšʼ', 'šʼšʼ')
        req = req.replace('zžʼ', 'žʼžʼ')
        req = rxCyrMultSoften.sub('ʼ', req)
        req = rxCyrVSoft.sub('\\1', req)
        return req

def writefile(name, text):
    fw = open(name, 'w', encoding = 'utf-8')
    fw.write(text) 
    fw.close()

A = []
string = ''
row = '%s\t%s\t%s\n'
for i in ['ADJ', 'IMIT', 'N', 'N_persn', 'NRel', 'PRO', 'unchangeable', 'V']:
    A += makedict(openfile('udm_lexemes_{}.txt'.format(i)))
#f = open('udmlexemes.tsv', 'r', encoding = 'utf-8')
#A = []
#string = ''
#row = '%s\t%s\t%s\t%s'
trans = []
for el in A:
    a = []
    a.append(convert_input(el[0], 'cyr'))
    a += el#.append(wordNew)
  #  a.append(line[0])
  #  a.append(line[1])
  #  a.append(line[2])
    trans.append(a)
for el in trans:
    string += '\t'.join(el)
    string += '\n'
#writefile('dict_udm.json', json.dumps(d, ensure_ascii=False))
writefile('udmlex.tsv', string)
#f.close()