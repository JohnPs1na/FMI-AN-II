import cProfile
import random
from collections import deque

"""
ncalls: numărul de apeluri
tottime: timpul total (agregat) în care a fost executată funcția curentă
percall: Raportul dintre timpul total și numărul de apeluri (cât a durat în medie o executare a acelei funcții\
cumtime: Timpul cumulat al executării funcției, împreună cu funcțiile apelate de către ea
percall: Se referă la al doilea percall din raport. Reprezintă raportul dintre timpul cumulat (cumtime) și numărul de apeluri (ncalls)
filename_lineno(function): Punctual din program, care a fost evaluat ( de exemplu un număr de linie din program sau un apel de funcție).


"""

"""
Observatie pentru cei absenti la laborator: trebuie sa dati enter după fiecare afișare a cozii/stivei până vă apare o soluție. Afișarea era ca să vedem progresul algoritmului. Puteți să o dezactivați comentând print-ul cu coada/stiva și infasuratoare.in()

De asemenea, apelurile algoritmilor sunt la final. Este doar unul dintre ele decomentat. Voi trebuie sa comentati/decomentati apelurile în funcție de ce vă interesează sa rulați.
"""


# informatii despre un nod din arborele de parcurgere (nu din graful initial)
class NodParcurgere:
    def __init__(self, id, info, parinte):
        self.id = id  # este indicele din vectorul de noduri
        self.info = info
        self.parinte = parinte  # parintele din arborele de parcurgere

    def obtineDrum(self):
        l = [self.info]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte.info)
            nod = nod.parinte
        return l

    def afisDrum(self):  # returneaza si lungimea drumului
        l = self.obtineDrum()
        print("->".join(l))
        return len(l)

    def contineInDrum(self, infoNodNou):
        # return infoNodNou in self.obtineDrum()
        nodDrum = self
        while nodDrum is not None:
            if (infoNodNou == nodDrum.info):
                return True
            nodDrum = nodDrum.parinte

        return False

    def __repr__(self):
        sir = ""
        sir += self.info + "("
        sir += "id = {}, ".format(self.id)
        sir += "drum="
        drum = self.obtineDrum()
        sir += ("->").join(drum)
        sir += ")"
        return (sir)


class Graph:  # graful problemei
    def __init__(self, noduri, matrice, start, scopuri):
        self.noduri = noduri
        self.matrice = matrice
        self.nrNoduri = len(matrice)
        self.start = start  # informatia nodului de start
        self.scopuri = scopuri  # lista cu informatiile nodurilor scop

    def indiceNod(self, n):
        return self.noduri.index(n)

    # va genera succesorii sub forma de noduri in arborele de parcurgere
    def genereazaSuccesori(self, nodCurent):
        listaSuccesori = []
        for i in range(self.nrNoduri):
            if self.matrice[nodCurent.id][i] == 1 and not nodCurent.contineInDrum(self.noduri[i]):
                nodNou = NodParcurgere(i, self.noduri[i], nodCurent)
                listaSuccesori.append(nodNou)
        return listaSuccesori

    def testeaza_scop(self, nodCurent):
        return nodCurent.info in self.scopuri;

    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return (sir)


##############################################################################################
#                                 Initializare problema                                      #
##############################################################################################

# pozitia i din vectorul de noduri da si numarul liniei/coloanei corespunzatoare din matricea de adiacenta
noduri = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
dictionar_counter_dfi = {}
for i in noduri:
    dictionar_counter_dfi[i] = 0

m = [
    [0, 1, 0, 1, 1, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 1, 0, 1, 0, 0],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 1, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
]

start = "a"
scopuri = ["f", "j"]
gr = Graph(noduri, m, start, scopuri)


#### algoritm BF
# presupunem ca vrem mai multe solutii (un numar fix) prin urmare vom folosi o variabilă numită nrSolutiiCautate
# daca vrem doar o solutie, renuntam la variabila nrSolutiiCautate
# si doar oprim algoritmul la afisarea primei solutii

def breadth_first(gr, nrSolutiiCautate=1):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(gr.noduri.index(gr.start), gr.start, None)]

    while len(c) > 0:
        print("Coada actuala: " + str(c))
        input()
        nodCurent = c.pop(0)

        lSuccesori = gr.genereazaSuccesori(nodCurent)
        c.extend(lSuccesori)
        for i in lSuccesori:
            if gr.testeaza_scop(i):
                print("Solutie:")
                i.afisDrum()
                print("\n----------------\n")
                input()
                nrSolutiiCautate -= 1
                if nrSolutiiCautate == 0:
                    return


def bf_queue(gr, nrSolutiiCautate=1):
    que = deque()
    que.append(NodParcurgere(gr.noduri.index(gr.start), gr.start, None))

    while que:
        print("Coada Actuala ", list(que))
        input()
        nod = que.popleft()
        lst, nrSolutiiCautate = gr.genereazaSuccesori(nod, nrSolutiiCautate)
        for i in lst:
            que.append(i)
        if nrSolutiiCautate == 0:
            return


def depth_first(gr, nrSolutiiCautate=1):
    # vom simula o stiva prin relatia de parinte a nodului curent
    df(NodParcurgere(gr.noduri.index(gr.start), gr.start, None), nrSolutiiCautate)


def df(nodCurent, nrSolutiiCautate):
    print(nodCurent.parinte, "Se expandeaza ->", nodCurent)
    if nrSolutiiCautate <= 0:  # testul acesta s-ar valida doar daca in apelul initial avem df(start,if nrSolutiiCautate=0)
        return nrSolutiiCautate
    print("Stiva actuala: " + "->".join(nodCurent.obtineDrum()))
    input()
    if gr.testeaza_scop(nodCurent):
        print("Solutie: ", end="")
        nodCurent.afisDrum()
        print("\n----------------\n")
        input()
        nrSolutiiCautate -= 1
        if nrSolutiiCautate == 0:
            return nrSolutiiCautate
    lSuccesori = gr.genereazaSuccesori(nodCurent)
    for sc in lSuccesori:
        if nrSolutiiCautate != 0:
            nrSolutiiCautate = df(sc, nrSolutiiCautate)

    print(nodCurent, "Se intoarce ->", nodCurent.parinte)
    return nrSolutiiCautate


# df(a)->df(b)->df(c)
#############################################


def dfi(nodCurent, adancime, nrSolutiiCautate):
    print("Stiva actuala: " + "->".join(nodCurent.obtineDrum()))
    input()
    if adancime == 1 and gr.testeaza_scop(nodCurent):
        print("Solutie: ", end="")
        nodCurent.afisDrum()
        print(dictionar_counter_dfi)
        for i in dictionar_counter_dfi:
            dictionar_counter_dfi[i] = 0
        print("\n----------------\n")
        input()
        nrSolutiiCautate -= 1
        if nrSolutiiCautate == 0:
            return nrSolutiiCautate
    if adancime > 1:
        lSuccesori = gr.genereazaSuccesori(nodCurent)
        for sc in lSuccesori:
            if nrSolutiiCautate != 0:
                dictionar_counter_dfi[nodCurent.info] += 1
                nrSolutiiCautate = dfi(sc, adancime - 1, nrSolutiiCautate)
    return nrSolutiiCautate


def depth_first_iterativ(gr, nrSolutiiCautate=1):
    for i in range(1, gr.nrNoduri + 1):
        if nrSolutiiCautate == 0:
            return
        print("**************\nAdancime maxima: ", i)
        nrSolutiiCautate = dfi(NodParcurgere(gr.noduri.index(gr.start), gr.start, None), i, nrSolutiiCautate)


"""
Mai jos puteti comenta si decomenta apelurile catre algoritmi. Pentru moment e apelat doar breadth-first
"""

# breadth_first(gr, nrSolutiiCautate=4)
# cProfile.run("breadth_first(gr, nrSolutiiCautate=4)")
####################################################


# depth_first(gr, nrSolutiiCautate=5)

# cProfile.run("depth_first(gr, nrSolutiiCautate=5)")
##################################################

# depth_first_iterativ(gr, nrSolutiiCautate=4)
# print(dictionar_counter_dfi)

#######################################################
#######################################################
#######################################################

# Lucru acasa
# EX 4 5 pe acasa

# Generare graf

numar_noduri = random.randint(18, 23)
adjacency_matrix = [[0 for i in range(numar_noduri)] for j in range(numar_noduri)]
graful_meu = [chr(ord('a') + i) for i in range(numar_noduri)]

nr_noduri_scop = random.randint(4, 7)

noduri_scop = []
while len(noduri_scop) != nr_noduri_scop:
    nod = random.randint(0, numar_noduri - 1)
    if graful_meu[nod] not in noduri_scop:
        noduri_scop.append(graful_meu[nod])

nr_muchii = 0

for i in range(numar_noduri):
    for j in range(numar_noduri):
        muc = random.randint(0, 1)
        adjacency_matrix[i][j] = muc
        if muc:
            nr_muchii += 1

g = Graph(graful_meu, adjacency_matrix, "a", noduri_scop)

print(g)


# print(graful_meu)
# print(nr_muchii)
# for i in adjacency_matrix:
#     print(i)

def Home_DFS_IterativStiva(gr, nrSolutiiCautate=5):
    visited = [0] * (gr.nrNoduri + 1)
    stiva = [NodParcurgere(gr.noduri.index(gr.start), gr.start, None)]

    total_Solutii = 0
    while len(stiva) and total_Solutii != nrSolutiiCautate:
        nodCurent = stiva[len(stiva) - 1]
        visited[nodCurent.id] = 1

        if gr.testeaza_scop(nodCurent):
            print("solutie:")
            nodCurent.afisDrum()
            total_Solutii += 1

        lSuccesori = gr.genereazaSuccesori(nodCurent)
        ok = 0

        for neighbor in lSuccesori:
            if visited[neighbor.id] == 0:
                stiva.append(neighbor)
                ok = 1
                break
        if ok:
            continue
        stiva.pop()

def Home_DFS_IterativDeque(gr, nrSolutiiCautate=5):
    visited = [0] * (gr.nrNoduri + 1)
    que = deque()
    que.append(NodParcurgere(gr.noduri.index(gr.start), gr.start, None))

    total_Solutii = 0
    while que and total_Solutii != nrSolutiiCautate:
        nodCurent = que[len(que) - 1]
        visited[nodCurent.id] = 1

        if gr.testeaza_scop(nodCurent):
            print("solutie:")
            nodCurent.afisDrum()
            total_Solutii += 1

        lSuccesori = gr.genereazaSuccesori(nodCurent)
        ok = 0

        for neighbor in lSuccesori:
            if visited[neighbor.id] == 0:
                que.append(neighbor)
                ok = 1
                break
        if ok:
            continue
        que.pop()


Home_DFS_IterativDeque(g,5)
