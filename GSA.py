import fileinput
import json
import time

def odredi_prazne_znakove(analizator_data):
    dodan = True
    prazni = []
    while dodan:
        #time.sleep(1)
        #print(prazni)
        dodan = False
        #print(analizator_data['nezavrsni_znakovi'])
        for nezavrsni in analizator_data['nezavrsni_znakovi']:
            if nezavrsni in prazni:
                continue
            #print(analizator_data['gramatike'][nezavrsni])
            for desna_strana in analizator_data['gramatike'][nezavrsni]:
                #print(desna_strana)
                if '$' in desna_strana and len(desna_strana) == 1:
                    dodan = True
                    prazni.append(nezavrsni)
                    continue
                nisu_svi_prazni = False
                for znak in desna_strana:
                    if znak not in prazni:
                        nisu_svi_prazni = True
                if not nisu_svi_prazni:
                    prazni.append(nezavrsni)
                    dodan = True
    return prazni

def zapocinje_izravno_znakom(A, B, analizator_data):

    zapocinje = 0
    prazni_znakovi = odredi_prazne_znakove(analizator_data)
    #print(prazni_znakovi)
    for produkcija in analizator_data['gramatike'][A]:
        temp_zapocinje = 1
        #print(produkcija)
        for znak in produkcija:
            if znak == B:
                break
            if znak not in prazni_znakovi:
                #print(znak, "nije")
                temp_zapocinje = 0
        if temp_zapocinje:
            zapocinje = 1
    return zapocinje

def zapocinje_znakom(tablica_zapocinjanja):
    for j in range(len(tablica_zapocinjanja)):
        for k in range(len(tablica_zapocinjanja)):
            for l in range(len(tablica_zapocinjanja)):
                if tablica_zapocinjanja[j][k] == 1 and tablica_zapocinjanja [k][l] == 1\
                        or j == l:
                    tablica_zapocinjanja[j][l] = 1
    return tablica_zapocinjanja

def indeks_znaka(znak, analizator_data):
    if znak in analizator_data['nezavrsni_znakovi']:
        return analizator_data['nezavrsni_znakovi'].index(znak)
    else:
        return len(analizator_data['nezavrsni_znakovi']) + analizator_data['zavrsni_znakovi'].index(znak)

#def znak_indeks(indeks, analizator_data):
    #if

def zapocinje(analizator_data):
    tablica_zapocinjanja = [[0 for i in range(len(analizator_data['nezavrsni_znakovi'])+len(analizator_data['zavrsni_znakovi']))] for j in range(len(analizator_data['nezavrsni_znakovi'])+len(analizator_data['zavrsni_znakovi']))]
    #print(tablica_zapocinjanja)
    i,j = 0,0
    for A in analizator_data['nezavrsni_znakovi']:
        j = 0
        for B in analizator_data['nezavrsni_znakovi'] + analizator_data['zavrsni_znakovi']:
            tablica_zapocinjanja[i][j] = zapocinje_izravno_znakom(A,B, analizator_data)
            j += 1
        i += 1

    tablica_zapocinjanja = zapocinje_znakom(tablica_zapocinjanja)

    #for i in range(len(tablica_zapocinjanja)):
    #    print(tablica_zapocinjanja[i])
    #print(indeks_znaka("<B>", analizator_data))
    return tablica_zapocinjanja
    #[indeks_znaka(nezavrsni_znak, analizator_data)][indeks_znaka(zavrsni_znak, analizator_data)]

def zapocinje_niz(niz_znakova, analizator_data):
    sviznakovi = analizator_data['nezavrsni_znakovi'] + analizator_data['zavrsni_znakovi']
    tablica_zapocinjanja = zapocinje(analizator_data)
    niz_zapocinje = []
    for znak1 in niz_znakova:
        for znak2 in sviznakovi:
            if tablica_zapocinjanja[sviznakovi.index(znak1)][sviznakovi.index(znak2)] and znak2 not in niz_zapocinje:
                niz_zapocinje.append(znak2)
    for i in range(len(tablica_zapocinjanja)):
        print(tablica_zapocinjanja[i])
    return niz_zapocinje

def zatvorenje_seta_LR_stavki(inicijalna_stavka,analizator_data)->set:
    zatvorenje = dict()
    (key_inic, lookback) = incijalna_stavka
    #zatvorenje =
    for ((lijevo, desno),lookback) in zatvorenje:
        sljedeci_znak_index = desno.index('tocka')+1
        if len(desno)> sljedeci_znak_index:
            if len(desno[sljedeci_znak_index])>=1 or desno[sljedeci_znak_index][0]!='<':
                continue
        delta = desno[sljedeci_znak_index+1:]+[lookback]
        zapocinje_delta_zavrsni = zapocinje_niz(delta, analizator_data)
        novo_lijevo = desno[sljedeci_znak_index]
        for produkcija in analizator_data['gramatike'][desno[sljedeci_znak_index]]:
            novo_desno = ['tocka'] + produkcija
            #novi_lookback =
        continue
    return set()

def generiraj_epsilon_nka(analizator_data)->dict:
    prazni_znakovi = odredi_prazne_znakove(analizator_data)
    epsilon_nka = dict()
    epsilon_nka['Sigma'] = analizator_data['nezavrsni_znakovi']+analizator_data['zavrsni_znakovi']
    epsilon_nka['Delta'] = dict()
    # Korak A
    pocetno_stanje = (('S\'', tuple(['tocka', analizator_data['nezavrsni_znakovi'][0]])), frozenset({''}))
    epsilon_nka['Q'] = {pocetno_stanje}
    epsilon_nka['q_0'] = pocetno_stanje
    red_stanja_b = [pocetno_stanje]
    red_stanja_c = [pocetno_stanje]
    while red_stanja_b or red_stanja_c:
        print()
        if red_stanja_b:
            # Korak B
            q = ((lijevo, desno_tup),lookback) = red_stanja_b.pop(0)
            desno = list(desno_tup)
            if len(desno) == 0: continue
            if desno[-1]=='tocka': continue
            tocka_index = desno.index('tocka')
            desno_delta = []
            if desno[tocka_index+1]!='$' and len(desno)> tocka_index+2:
                desno_delta = desno[:tocka_index] + [desno[tocka_index+1],desno[tocka_index]] + desno[tocka_index+2:]
            if desno[tocka_index+1]=='$' and len(desno)> tocka_index+2:
                desno_delta = desno[:tocka_index+1] + desno[tocka_index+2:]
            if desno[tocka_index+1]!='$' and len(desno)<=tocka_index+2:
                desno_delta = desno[:tocka_index] + [desno[tocka_index+1],desno[tocka_index]]
            if desno[tocka_index+1]=='$' and len(desno)<=tocka_index+2:
                desno_delta = desno[:tocka_index]
            q_delta = ((lijevo, tuple(desno_delta)), lookback)
            Q_stara_velicina = len(epsilon_nka['Q'])
            epsilon_nka['Q'].add(q_delta)
            epsilon_nka['Delta'][(q,desno[1])] = {q_delta}
            if len(epsilon_nka['Q']) == Q_stara_velicina: continue
            print('B: ',q_delta)
            red_stanja_b.append(q_delta)
            red_stanja_c.append(q_delta)
        if red_stanja_c:
            # Korak C
            q = ((lijevo, desno_tup),lookback) = red_stanja_c.pop(0)
            desno = list(desno_tup)
            if desno[-1]=='tocka': continue
            tocka_index = desno.index('tocka')
            if not desno[tocka_index+1] in analizator_data['nezavrsni_znakovi']: continue
            gramatike = analizator_data['gramatike'][desno[tocka_index+1]]
            Q_delta = set()
            lijevo_delta = desno[tocka_index+1]
            T = set()
            if tocka_index+2>=len(desno):
                T.update(lookback)
            else:
                b_1 =[znak for znak in zapocinje_niz(desno[tocka_index+2:],analizator_data) if znak in analizator_data['zavrsni_znakovi']]
                T.update(set(b_1))
                beta_moze_biti_prazna =  len(set(desno[tocka_index+2:]) & set(prazni_znakovi))==len(set(desno[tocka_index+2:]))
                if beta_moze_biti_prazna:
                    T.update(lookback)
            for gramatika in gramatike:
                q_delta_novi = ()
                if gramatika==['$']:
                    q_delta_novi = ((lijevo_delta,tuple(['tocka'])),frozenset(T))
                else:
                    q_delta_novi = ((lijevo_delta,tuple(['tocka']+gramatika)),frozenset(T))
                Q_delta.add(q_delta_novi)
                Q_stara_velicina = len(epsilon_nka['Q'])
                epsilon_nka['Q'].add(q_delta_novi)
                if len(epsilon_nka['Q']) == Q_stara_velicina: continue
                print('C: ',q_delta_novi)
                red_stanja_b.append(q_delta_novi)
                red_stanja_c.append(q_delta_novi)
            epsilon_nka['Delta'][(q,'')] = Q_delta
    epsilon_nka['F'] = epsilon_nka['Q']
    return epsilon_nka

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

    #print(automat["pocetni"])


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

    #print([(k,v) for k,values in LR_stavke.items() for v in values])
    #print(next(iter(LR_stavke)))
    #print("ODREDI ZAPOCINJANJE")
    #print(zapocinje_niz(["<A>", "<B>", "<D>"],analizator_data))
    #print(zapocinje_izravno_znakom(analizator_data['nezavrsni_znakovi'][1], analizator_data['nezavrsni_znakovi'][0], analizator_data))
    napravi_epsilon_NKA(analizator_data, LR_stavke)

    with open('analizator/analizator_data.json', 'w') as file_analizator:
        json.dump(analizator_data, file_analizator, indent=2)

