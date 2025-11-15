import fileinput
import json

def stvori_LR_stavke(produkcije):
    LR_stavke = []
    for lista in produkcije:
        for i in range(len(lista)+1):
            temp = lista.copy()
            temp.insert(i, "tocka")
            LR_stavke.append(temp)
    return LR_stavke

def napravi_epsilon_NKA(gramatika, LR_stavke):
    automat = dict()
    ulazni_znakovi = gramatika['nezavrsni_znakovi'] + gramatika['zavrsni_znakovi']
    automat["pocetni"] = [next(iter(gramatika['nezavrsni_znakovi'])), LR_stavke[next(iter(gramatika['nezavrsni_znakovi']))][0]]

    print(automat["pocetni"])


if __name__ == '__main__':
    analizator_data = dict()
    analizator_data['nezavrsni_znakovi'] = []
    analizator_data['zavrsni_znakovi'] = []
    analizator_data['sinkronizacijski_znakovi'] = []
    analizator_data['gramatike'] = dict()
    lijeva:str = ""
    for line in fileinput.input():
        if line[1] == 'V':
            analizator_data['nezavrsni_znakovi'] = line.rstrip("\n").rstrip("\r").split(' ')[1:]
            continue
        if line[1] == 'T':
            analizator_data['zavrsni_znakovi'] = line.rstrip("\n").rstrip("\r").split(' ')[1:]
            continue
        if line[1] == 'S':
            analizator_data['sinkronizacijski_znakovi'] = line.rstrip("\n").rstrip("\r").split(' ')[1:]
            continue

        if line[0] == '<':
            lijeva = line.rstrip("\n").rstrip("\r")
        else:
            analizator_data['gramatike'].setdefault(lijeva,[])
            analizator_data['gramatike'][lijeva].append(line.rstrip("\n").rstrip("\r").lstrip(" ").split(' '))



    znakovi = analizator_data['nezavrsni_znakovi']
    LR_stavke = dict()
    for znak in znakovi:
        LR_stavke[znak] = stvori_LR_stavke(analizator_data['gramatike'][znak])
    #print(next(iter(LR_stavke)))

    napravi_epsilon_NKA(analizator_data, LR_stavke)

    with open('analizator/analizator_data.json', 'w') as file_analizator:
        json.dump(analizator_data, file_analizator, indent=2)
