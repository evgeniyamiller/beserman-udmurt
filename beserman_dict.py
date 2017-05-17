from lxml import etree

def xml2arr():
    doc = etree.parse('tlex-2016.10.19.xml')
    arr = []

    nodes = doc.xpath('//Lemma')
    for node in nodes:
        lex = node.get('LemmaSign')
        udmortho = node.xpath("Udmurt/@UdmurtOrtho")
        value = node.xpath("PSBlock/Value/@ValTr")
        if value == []: value = node.xpath("PSBlock/Value/@ValTolk")
        ps = node.xpath("PSBlock/@PsbPS")
        arr.append([lex, ', '.join(udmortho), '; '.join(value), '; '.join(ps)])

    return arr

def lex_split(arr):
    D = {k:[] for k in ['N', 'IMIT', 'V']}
    row = '%s\t%s\t%s\t%s\n'
    
    for line in arr:
        parts = []
        if "172" in line[3] or '181' in line[3] or '192' in line[3] or '612' in line[3] or '0' in line[3]:
            parts.append('N')
        if '173' in line[3] or '613' in line[3]:
            parts.append('ADJ')
        if '171' in line[3] or '174' in line[3]:
            parts.append('ADV')
        if "191" in line[3] or '194' in line[3]:
            parts.append('V')
        if '187' in line[3] or '612' in line[3] or '613' in line[3]:
            parts.append('POST')
        if '177' in line[3] or '186' in line[3] or '188' in line[3] or '190' in line[3]:
            parts.append('PRO')
        if '182' in line[3] or '183' in line[3]:
            parts.append('NUM')
        if '194' in line[3]:
            parts.append('PRAED')
        if '180' in line[3]:
            parts.append('INTRJ')
        if '176' in line[3]:
            parts.append('CNJ')
        if '178' in line[3]:
            parts.append('IMIT')
        if '185' in line[3]:
            parts.append('PART')
        if 'N' in parts or 'ADJ' in parts or 'ADV' in parts or 'POST' in parts or 'PRO' in parts or 'NUM' in parts or 'PRAED' in parts or 'INTRJ' in parts or 'CNJ' in parts or 'PART' in parts:
            D['N'].append(row % (line[0], line[1], line[2], ', '.join(parts)))
        if 'V' in parts or 'PRAED' in parts:
            D['V'].append(row % (line[0], line[1], line[2], ', '.join(parts)))
        if 'IMIT' in parts:
            D['IMIT'].append(row % (line[0], line[1], line[2], ', '.join(parts)))
    return D

def main():
    D = lex_split(xml2arr())
    for k in D:
        fw = open('beslex_' + k + '.tsv', 'w', encoding = 'utf-8')
        fw.write(''.join(D[k]))
        fw.close()

if __name__ == '__main__':
    main()


