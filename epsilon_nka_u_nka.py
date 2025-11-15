from itertools import chain
from pprint import pprint

def epsilon_okruzenje(epsilon_nka:dict,q) -> set:
    e_okruzenje= {q}
    stog = [q]
    while stog:
        q = stog.pop()
        for q_delta in epsilon_nka['Delta'].get((q,''),[]):
            if q_delta in e_okruzenje:
                continue
            e_okruzenje.add(q_delta)
            stog.append(q_delta)
    return e_okruzenje

def epsilon_okruzenja(epsilon_nka:dict) -> dict:
    e_okruzenja = dict()
    for q in epsilon_nka['Q']:
        e_okruzenja[q] = epsilon_okruzenje(epsilon_nka,q)
    return e_okruzenja

def epsilon_nka_u_nka(epsilon_nka:dict) -> dict:
    nka = dict()
    e_okruzenja = epsilon_okruzenja(epsilon_nka)
    nka['Q'] = e_okruzenja.values()
    nka['q_0'] = e_okruzenja[epsilon_nka['q_0']]
    nka['F'] = {q for q in nka['Q'] if set(epsilon_nka['F']) & q}
    nka['Sigma'] = epsilon_nka['Sigma']
    nka['Delta'] = dict()
    for q in nka['Q']:
        for sigma in nka['Sigma']:
            Q_delta = set()
            for q_e in q:
                Q_e_delta = epsilon_nka['Delta'].get((q_e,sigma),{})
                for q_e_delta in Q_e_delta:
                    Q_delta.update(e_okruzenja.get(q_e_delta,{}))
            if Q_delta:
                nka['Delta'][(q,sigma)] = Q_delta
    return nka

if __name__ == '__main__':
    epsilon_nka ={
        'Q': {'q0','q1','q2','q3','q4'},
        'q_0': 'q0',
        'F': {'q3'},
        'Sigma': {'0','1'},
        'Delta': {
            ('q0','1'): {'q1','q2'},
            ('q1','0'): {'q0'},
            ('q2','1'): {'q2'},
            ('q3','0'): {'q3'},
            ('q0',''): {'q3'},
            ('q3',''): {'q1'},
            ('q2',''): {'q4'},
            ('q4','1'): {'q1'},
        },
    }
    pprint(epsilon_nka_u_nka(epsilon_nka))