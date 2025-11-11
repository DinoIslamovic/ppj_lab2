import fileinput
import json

if __name__ == '__main__':
    analizator_data = dict()
    analizator_data['nezavrsni_znakovi'] = []
    analizator_data['zavrsni_znakovi'] = []
    analizator_data['sinkronizacijski_znakovi'] = []
    analizator_data['gramatike'] = dict()
    lijeva:str = ""
    for line in fileinput.input():
        if line[1] == 'V':
            analizator_data['nezavrsni_znakovi'].append(line.rstrip("\n").split(' ')[1:])
            continue
        if line[1] == 'T':
            analizator_data['zavrsni_znakovi'].append(line.rstrip("\n").split(' ')[1:])
            continue
        if line[1] == 'S':
            analizator_data['sinkronizacijski_znakovi'].append(line.rstrip("\n").split(' ')[1:])
            continue

        if line[0] == '<':
            lijeva = line.rstrip("\n")
        else:
            analizator_data['gramatike'].setdefault(lijeva,[])
            analizator_data['gramatike'][lijeva].append(line.rstrip("\n").lstrip(" ").split(' '))

    with open('analizator/analizator_data.json', 'w') as file_analizator:
        json.dump(analizator_data, file_analizator, indent=2)
