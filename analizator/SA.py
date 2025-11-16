import json
import fileinput


if __name__ == '__main__':
    uniformni_izrazi = []
    for line in fileinput.input():
        uniformni_izrazi.append(line.split())
    print(uniformni_izrazi)

    analizator_data: dict = {}
    with open('analizator_data.json', 'r') as f:
        analizator_data = json.load(f)
        print(analizator_data)

    tablica_akcija = []
    with open('tablica_akcija.txt', 'r') as tablica_akcija_file:
        for line in tablica_akcija_file:
            #print(line.rstrip("\n").rstrip("\r"))
            temp = []
            for stavka in line.rstrip("\n").rstrip("\r").split():
                temp += [stavka]
            tablica_akcija += [temp]
        print(tablica_akcija)

    tablica_ns = []
    with open('tablica_ns.txt', 'r') as tablica_ns_file:
        for line in tablica_ns_file:
            # print(line.rstrip("\n").rstrip("\r"))
            temp = []
            for stavka in line.rstrip("\n").rstrip("\r").split():
                temp += [stavka]
            tablica_ns += [temp]
        print(tablica_ns)