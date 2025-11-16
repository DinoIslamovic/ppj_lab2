from itertools import chain
from pprint import pprint


def epsilon_okruzenje(epsilon_nka: dict, q) -> frozenset:
    e_okruzenje = {q}
    stog = [q]
    while stog:
        q = stog.pop()
        for q_delta in epsilon_nka['Delta'].get((q, ''), []):
            if q_delta in e_okruzenje:
                continue
            e_okruzenje.add(q_delta)
            stog.append(q_delta)
    return frozenset(e_okruzenje)


def epsilon_okruzenje_list(epsilon_nka: dict, Q) -> set:
    e_okruzenje = set()
    for q in Q:
        e_okruzenje.update(epsilon_okruzenje(epsilon_nka, q))
    return e_okruzenje


def epsilon_okruzenja(epsilon_nka: dict) -> dict:
    e_okruzenja = dict()
    for q in epsilon_nka['Q']:
        e_okruzenja[q] = epsilon_okruzenje(epsilon_nka, q)
    return e_okruzenja


def epsilon_nka_u_nka(epsilon_nka: dict) -> dict:
    nka = dict()
    e_okruzenja = epsilon_okruzenja(epsilon_nka)
    nka['Q'] = frozenset(e_okruzenja.values())
    nka['q_0'] = e_okruzenja[epsilon_nka['q_0']]
    nka['F'] = frozenset({q for q in nka['Q'] if set(epsilon_nka['F']) & q})
    nka['Sigma'] = epsilon_nka['Sigma']
    nka['Delta'] = dict()
    for q in nka['Q']:
        for sigma in nka['Sigma']:
            Q_delta = set()
            for q_e in q:
                Q_e_delta = epsilon_nka['Delta'].get((q_e, sigma), {})
                for q_e_delta in Q_e_delta:
                    Q_delta.update(e_okruzenja.get(q_e_delta, {}))
            if Q_delta:
                nka['Delta'][(q, sigma)] = frozenset(Q_delta)
    return nka


def epsilon_nka_u_dka(epsilon_nka: dict) -> dict:
    dka = dict()
    dka['q_0'] = frozenset(epsilon_okruzenje(epsilon_nka, epsilon_nka['q_0']))
    dka['Q'] = {dka['q_0']}
    dka['Sigma'] = epsilon_nka['Sigma']
    dka['Delta'] = dict()
    dka['F'] = set()
    queue = [dka['q_0']]
    if dka['q_0'] & epsilon_nka['F']:
        dka['F'].add(dka['q_0'])
    while queue:
        q = queue.pop(0)
        for sigma in dka['Sigma']:
            dka['Delta'][(q, sigma)] = set()
            for q_e in q:
                if (q_e, sigma) in epsilon_nka['Delta']:
                    dka['Delta'][(q, sigma)].update(epsilon_nka['Delta'][(q_e, sigma)])
            dka['Delta'][(q, sigma)] = frozenset(epsilon_okruzenje_list(epsilon_nka, dka['Delta'][(q, sigma)]))
            if dka['Delta'][(q, sigma)] not in dka['Q'] and dka['Delta'][(q, sigma)]:
                dka['Q'].add(dka['Delta'][(q, sigma)])
                queue.append(dka['Delta'][(q, sigma)])
                if dka['Delta'][(q, sigma)] & epsilon_nka['F']:
                    dka['F'].add(dka['Delta'][(q, sigma)])
            if not dka['Delta'][(q, sigma)]:
                dka['Delta'].pop((q, sigma))
    return dka


def epsilon_nka_u_tablicu(epsilon_nka: dict):
    dka = epsilon_nka_u_dka(epsilon_nka)
    q_to_id = dict()
    id_to_q = []
    q_to_id[dka['q_0']] = 0
    id_to_q.append(dka['q_0'])
    for q in dka['Q']:
        if q == dka['q_0']:
            continue
        q_to_id[q] = len(id_to_q)
        id_to_q.append(q)
    tablica = dict()

    for ((q, sigma), q_delta) in dka['Delta'].items():
        if sigma[0] == '<' and sigma[-1] == '>' or sigma == 'S\'':
            tablica[(q_to_id[q], sigma)] = ('Stavi', q_to_id[q_delta])
            continue
        for ((lijevo, desno), loopback) in q:
            if lijevo == 'S\'' and desno[:-1] == 'tocka':
                tablica[(q_to_id[q], '')] = 'Prihvati'
            if desno[-1] == 'tocka':
                for a in loopback:
                    if desno[:-1]:
                        tablica[(q_to_id[q], a)] = ('Reduciraj', lijevo, list(desno[:-1]))
                    else:
                        tablica[(q_to_id[q], a)] = ('Reduciraj', lijevo, [''])
                continue
            znak = desno[desno.index('tocka') + 1]
            if sigma != znak:
                continue
            if len(znak) == 1:
                tablica[(q_to_id[q], znak)] = ('Pomakni', q_to_id[q_delta])

    return tablica


def ispisi_deltu(dka):
    id_to_q = list(dka['Q'])
    q_to_id = dict()
    for i in range(0, len(id_to_q)):
        q_to_id[id_to_q[i]] = i
    for (lijevo, desno) in dka['Delta'].items():
        for q in desno:
            print(q_to_id[lijevo[0]], '->', lijevo[1], '->', q_to_id[q])


if __name__ == '__main__':

    epsilon_nka = {'Sigma': ['<S>', '<A>', '<B>', 'a', 'b'], 'Delta': {
        ((("S'", ('tocka', '<S>')), frozenset({''})), '<S>'): {(("S'", ('<S>', 'tocka')), frozenset({''}))},
        ((("S'", ('tocka', '<S>')), frozenset({''})), ''): {(('<S>', ('tocka', '<A>')), frozenset({''}))},
        ((('<S>', ('tocka', '<A>')), frozenset({''})), '<A>'): {(('<S>', ('<A>', 'tocka')), frozenset({''}))},
        ((('<S>', ('tocka', '<A>')), frozenset({''})), ''): {(('<A>', ('tocka', '<B>', '<A>')), frozenset({''})),
                                                             (('<A>', ('tocka',)), frozenset({''}))},
        ((('<A>', ('tocka', '<B>', '<A>')), frozenset({''})), '<B>'): {
            (('<A>', ('<B>', 'tocka', '<A>')), frozenset({''}))},
        ((('<A>', ('<B>', 'tocka', '<A>')), frozenset({''})), 'tocka'): {
            (('<A>', ('<B>', '<A>', 'tocka')), frozenset({''}))},
        ((('<A>', ('tocka', '<B>', '<A>')), frozenset({''})), ''): {
            (('<B>', ('tocka', 'a', '<B>')), frozenset({'', 'b', 'a'})),
            (('<B>', ('tocka', 'b')), frozenset({'', 'b', 'a'}))},
        ((('<B>', ('tocka', 'a', '<B>')), frozenset({'', 'b', 'a'})), 'a'): {
            (('<B>', ('a', 'tocka', '<B>')), frozenset({'', 'b', 'a'}))},
        ((('<B>', ('tocka', 'b')), frozenset({'', 'b', 'a'})), 'b'): {
            (('<B>', ('b', 'tocka')), frozenset({'', 'b', 'a'}))},
        ((('<A>', ('<B>', 'tocka', '<A>')), frozenset({''})), ''): {(('<A>', ('tocka', '<B>', '<A>')), frozenset({''})),
                                                                    (('<A>', ('tocka',)), frozenset({''}))},
        ((('<B>', ('a', 'tocka', '<B>')), frozenset({'', 'b', 'a'})), 'tocka'): {
            (('<B>', ('a', '<B>', 'tocka')), frozenset({'', 'b', 'a'}))},
        ((('<B>', ('a', 'tocka', '<B>')), frozenset({'', 'b', 'a'})), ''): {
            (('<B>', ('tocka', 'a', '<B>')), frozenset({'', 'b', 'a'})),
            (('<B>', ('tocka', 'b')), frozenset({'', 'b', 'a'}))}},
                   'Q': {(('<B>', ('tocka', 'b')), frozenset({'', 'b', 'a'})),
                         (('<A>', ('<B>', '<A>', 'tocka')), frozenset({''})),
                         (("S'", ('<S>', 'tocka')), frozenset({''})), (("S'", ('tocka', '<S>')), frozenset({''})),
                         (('<B>', ('a', 'tocka', '<B>')), frozenset({'', 'b', 'a'})),
                         (('<B>', ('a', '<B>', 'tocka')), frozenset({'', 'b', 'a'})),
                         (('<A>', ('tocka',)), frozenset({''})), (('<B>', ('b', 'tocka')), frozenset({'', 'b', 'a'})),
                         (('<S>', ('<A>', 'tocka')), frozenset({''})),
                         (('<A>', ('tocka', '<B>', '<A>')), frozenset({''})),
                         (('<A>', ('<B>', 'tocka', '<A>')), frozenset({''})),
                         (('<B>', ('tocka', 'a', '<B>')), frozenset({'', 'b', 'a'})),
                         (('<S>', ('tocka', '<A>')), frozenset({''}))},
                   'q_0': (("S'", ('tocka', '<S>')), frozenset({''})),
                   'F': { (('<B>', ('tocka', 'b')), frozenset({'', 'b', 'a'})),
                         (('<A>', ('<B>', '<A>', 'tocka')), frozenset({''})),
                         (("S'", ('<S>', 'tocka')), frozenset({''})), (("S'", ('tocka', '<S>')), frozenset({''})),
                         (('<B>', ('a', 'tocka', '<B>')), frozenset({'', 'b', 'a'})),
                         (('<B>', ('a', '<B>', 'tocka')), frozenset({'', 'b', 'a'})),
                         (('<A>', ('tocka',)), frozenset({''})), (('<B>', ('b', 'tocka')), frozenset({'', 'b', 'a'})),
                         (('<S>', ('<A>', 'tocka')), frozenset({''})),
                         (('<A>', ('tocka', '<B>', '<A>')), frozenset({''})),
                         (('<A>', ('<B>', 'tocka', '<A>')), frozenset({''})),
                         (('<B>', ('tocka', 'a', '<B>')), frozenset({'', 'b', 'a'})),
                         (('<S>', ('tocka', '<A>')), frozenset({''}))}}

    pprint('=====')
    pprint(epsilon_nka_u_dka(epsilon_nka)['Q'])
    pprint('=====')
    pprint(epsilon_nka_u_tablicu(epsilon_nka))
