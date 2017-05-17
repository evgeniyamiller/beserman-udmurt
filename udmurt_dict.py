from translit import convert_input

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

#alf = 'абвгдежзийклмнопрстуфхцчшыьёюяӧӝӟӵ'
#trans = list('abvgdežzijklmnoprstufxcčšə')
#trans.append('ə̂')
#trans.append('ə̈əɤ')

def dictionary():
    A = []
    for i in ['ADJ', 'IMIT', 'N', 'N_persn', 'NRel', 'PRO', 'unchangeable', 'V']:
        A += makedict(openfile('udm_lexemes_{}.txt'.format(i)))
    transl = []
    for el in A:
        a = []
        a.append(convert_input(el[0], 'cyr'))
        a += el
        transl.append(a)
    return transl

def dict_split(transl):
    D = {k:[] for k in ['N', 'IMIT', 'V']}
    row = '%s\t%s\t%s\t%s\n'
    for line in dictionary():
        parts = []
        if line[2] == 'N' or 'ADJ' in line[2]:
            parts.append(line[2])
        elif 'N-persn' in line[2] or 'N,' in line[2]:
            parts.append('N')
        elif 'V,' in line[2]:    
            parts.append('V')
        if 'ADV' in line[2]:
            parts.append('ADV')
        if 'POST' in line[2]:
            parts.append('POST')
        if 'PRO' in line[2]:
            parts.append('PRO')
        if 'NUM' in line[2]:
            parts.append('NUM')
        if 'INTRJ' in line[2]:
            parts.append('INTRJ')
        if 'CNJ' in line[2]:
            parts.append('CNJ')
        if 'IMIT' in line[2]:
            parts.append('IMIT')
        if 'PART' in line[2]:
            parts.append('PART')
        if 'N' in parts or 'ADJ' in parts or 'ADV' in parts or 'POST' in parts or 'PRO' in parts or 'NUM' in parts or 'PRAED' in parts or 'INTRJ' in parts or 'CNJ' in parts or 'PART' in parts:
            D['N'].append(row % (line[0], line[1], ', '.join(parts), line[3]))
        if 'V' in parts or 'PRAED' in parts:
            D['V'].append(row % (line[0], line[1], ', '.join(parts), line[3]))
        if 'IMIT' in parts:
            D['IMIT'].append(row % (line[0], line[1], ', '.join(parts), line[3]))
    return D

def main():
    D = dict_split(dictionary())        
    for k in D:
        D[k] = set(D[k])
        fw = open('udmlex_' + k + '.tsv', 'w', encoding = 'utf-8')
        fw.write(''.join(D[k]))
        fw.close()

if __name__ == '__main__':
    main()
