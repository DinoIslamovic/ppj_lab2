import json
import fileinput
from tablica import tablica

tablica_example = {
    (0, 'a'): ('Pomakni', 3),
    (0, 'b'): ('Pomakni', 4),
    (0, ''): ('Reduciraj', '<A>', ['']),
    (0, '<B>'): ('Stavi', 2),
    (0, '<A>'): ('Stavi', 1),
    (1, ''): ('Prihvati', -1),
    (2, 'a'): ('Pomakni', 3),
    (2, 'b'): ('Pomakni', 4),
    (2, ''): ('Reduciraj', '<A>', ['']),
    (2, '<B>'): ('Stavi', 2),
    (2, '<A>'): ('Stavi', 5),
    (3, 'a'): ('Pomakni', 3),
    (3, 'b'): ('Pomakni', 4),
    (3, '<B>'): ('Stavi', 6),
    (4, 'a'): ('Reduciraj', '<B>', ['b']),
    (4, 'b'): ('Reduciraj', '<B>', ['b']),
    (4, ''): ('Reduciraj', '<B>', ['b']),
    (5, ''): ('Reduciraj', '<A>', ['<B>', '<A>']),
    (6, 'a'): ('Reduciraj', '<B>', ['a', '<B>']),
    (6, 'b'): ('Reduciraj', '<B>', ['a', '<B>']),
    (6, ''): ('Reduciraj', '<B>', ['a', '<B>']),
}


def generiraj_stablo(uniformni_izrazi, tablica_akcija_ns, analizator_data):
    uniformni_izrazi.append(['', -1])
    pointer = 0
    stablo = []
    stog = ["DELTA", 0]
    while (True):
        read_znak = uniformni_izrazi[pointer].copy()
        read_stanje = stog[-1]
        procitaj = tablica_akcija_ns[read_stanje, read_znak[0]]

        naredba = procitaj[0]
        # print(stog)

        if naredba == 'Prihvati':
            print("success")
            break
        elif naredba == "Pomakni":
            stog += [read_znak]
            stog += [procitaj[1]]
            pointer += 1
        elif naredba == "Stavi":
            stog += [procitaj[1]]
        elif naredba == "Reduciraj":
            lista_znakova_za_reducirati = procitaj[2].copy()
            lista_znakova_za_reducirati.reverse()
            prijasnje = []
            while (len(lista_znakova_za_reducirati) > 0):
                stog.pop()  # stanje
                x = stog.pop()
                prijasnje = [x, 'novi_red'] + prijasnje  # znak #oporavak od greške
                if lista_znakova_za_reducirati[-1] == '':
                    prijasnje = prijasnje + [(procitaj[1], 'pod', ['$'])]
                lista_znakova_za_reducirati.pop()
            stog += [(procitaj[1], 'pod', prijasnje)]
            stog += [tablica_akcija_ns[stog[-2], procitaj[1]][1]]
        else:
            print(f"Odbacio na liniji {uniformni_izrazi[pointer][1]}!")
            svi_znakovi = analizator_data['nezavrsni_znakovi'] + analizator_data['zavrsni_znakovi'] + ['']
            valid_stanja = []
            for i in svi_znakovi:
                if (read_stanje, i) in tablica_akcija_ns.keys():
                    valid_stanja += [i]
            print(f'Očekivani su neki od ovih znakova:{valid_stanja}')
            print(f'Pročitan znak: {read_znak} := {uniformni_izrazi[pointer][2]}')

            x = '#)/$(&Q/%)(&)'
            while x not in analizator_data['sinkronizacijski_znakovi']:
                x = uniformni_izrazi[pointer][0]
                pointer+=1
            pointer -= 1

            valid_stanja = []
            broj_stanja = 0
            for (n,sigma) in tablica_akcija_ns.keys():
                broj_stanja = max(n,broj_stanja)
            broj_stanja+=1

            for i in range(broj_stanja):
                if (i, x) in tablica_akcija_ns.keys():
                    valid_stanja += [i]

            while stog[-2][0] not in valid_stanja:
                stog.pop()
                stog.pop()


    return stog


def print_stablo_drugo(stablo, indent=''):
    if isinstance(stablo, str):
        print(indent, stablo, sep='')
        return
    if isinstance(stablo, list):
        if isinstance(stablo[0], str):
            if len(stablo[0]) == 1:
                print(indent, ' '.join(stablo), sep='')
                return
    s = stablo
    pod = False
    novi_red = False
    for p in s:
        if p == 'pod':
            pod = True
            continue
        if p == 'novi_red':
            novi_red = True
            continue
        if (not pod and not novi_red) or novi_red:
            print_stablo_drugo(p, indent)
        if pod:
            print_stablo_drugo(p, indent + ' ')
            indent = indent[:-1]
            pod = False

    # print(s, end = '')


def print_stablo(stablo):
    # print(stablo)
    if isinstance(stablo, str):
        return stablo.rstrip("\n").rstrip("\r") + '\n'
    # print(stablo)
    nesto = ' '
    for i in stablo:
        nesto += ' ' + print_stablo(i)
    # nesto += '\n'
    print(nesto)
    return nesto

    return '\n'


if __name__ == '__main__':
    uniformni_izrazi = []
    for line in fileinput.input():
        uniformni_izrazi.append(line.split())
    # print(uniformni_izrazi)

    analizator_data: dict = {}
    with open('analizator_data.json', 'r') as f:
        analizator_data = json.load(f)
        # print(analizator_data)



    stablo = generiraj_stablo(uniformni_izrazi, tablica, analizator_data)
    # print(stablo[2:-1])
    # print(print_stablo(stablo[2:-1]))
    print_stablo_drugo(stablo[2])
