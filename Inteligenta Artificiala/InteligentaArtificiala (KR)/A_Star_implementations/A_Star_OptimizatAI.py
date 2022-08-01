"""
Observatie pentru cei absenti la laborator: trebuie sa dati enter după fiecare afișare a cozii până vă apare o soluție.
Afișarea era ca să vedem progresul algoritmului. Puteți să o dezactivați comentând print-ul cu coada și infasuratoare.in()
"""
import cProfile
import queue
# informatii despre un nod din arborele de parcurgere (nu din graful initial)
class NodParcurgere:
    graf = None  # static

    def __init__(self, id, info, parinte, cost, h):
        self.id = id  # este indicele din vectorul de noduri
        self.info = info
        self.parinte = parinte  # parintele din arborele de parcurgere
        self.g = cost  # costul de la radacina la nodul curent
        self.h = h
        self.f = self.g + self.h

    def obtineDrum(self):
        l = [self.info]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte.info)
            nod = nod.parinte
        return l

    def afisDrum(self):  # returneaza si lungimea drumului
        l = self.obtineDrum()
        print(("->").join(l))
        print("Cost: ", self.g)
        return len(l)

    def contineInDrum(self, infoNodNou):
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
        sir += " g:{}".format(self.g)
        sir += " h:{}".format(self.h)

        sir += " f:{})".format(self.f)
        return (sir)

    def __eq__(self, other):
        return self.f == other.f and self.g == other.g

    # observati ca nu trebuie sa ne raportam la aceleasi criterii, chiar daca in general nu este indicat
    def __lt__(self, other):
        if self.f < other.f:
            return True
        elif self.f == other.f:
            if self.g > other.g:
                return True
        return False


class Graph:  # graful problemei
    def __init__(self, noduri, matriceAdiacenta, matricePonderi, start, scopuri, lista_h):
        self.noduri = noduri
        self.matriceAdiacenta = matriceAdiacenta
        self.matricePonderi = matricePonderi
        self.nrNoduri = len(matriceAdiacenta)
        self.start = start
        self.scopuri = scopuri
        self.lista_h = lista_h

    def indiceNod(self, n):
        return self.noduri.index(n)

    def testeaza_scop(self, nodCurent):
        return nodCurent.info in self.scopuri;

    # va genera succesorii sub forma de noduri in arborele de parcurgere
    def genereazaSuccesori(self, nodCurent):
        listaSuccesori = []
        for i in range(self.nrNoduri):
            if self.matriceAdiacenta[nodCurent.id][i] == 1 and not nodCurent.contineInDrum(self.noduri[i]):
                nodNou = NodParcurgere(i, self.noduri[i], nodCurent, nodCurent.g + self.matricePonderi[nodCurent.id][i],
                                       self.calculeaza_h(self.noduri[i]))
                listaSuccesori.append(nodNou)
        return listaSuccesori

    def calculeaza_h(self, infoNod):
        return self.lista_h[self.indiceNod(infoNod)]

    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return (sir)


##############################################################################################
#                                 Initializare problema                                      #
##############################################################################################

# pozitia i din vectorul de noduri da si numarul liniei/coloanei corespunzatoare din matricea de adiacenta
noduri = ["a", "b", "c", "d", "e", "f", "g", "i", "j", "k"]

m = [
    [0, 1, 0, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
mp = [
    [0, 7, 0, 0, 5, 17, 0, 0, 0, 0],
    [0, 0, 0, 5, 0, 0, 3, 0, 0, 0],
    [0, 3, 0, 0, 0, 3, 0, 0, 0, 0],
    [0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 14, 9, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
start = "a"
scopuri = ["f"]
# exemplu de euristica banala (1 daca nu e nod scop si 0 daca este)
vect_h = [0, 8, 3, 5, 9, 0, 5, 0, 0, 0]

gr = Graph(noduri, m, mp, start, scopuri, vect_h)
NodParcurgere.graf = gr;


def a_star(gr):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    l_open = [NodParcurgere(gr.noduri.index(gr.start), gr.start, None, 0, gr.calculeaza_h(gr.start))]

    # l_open contine nodurile candidate pentru expandare (este echivalentul lui c din A* varianta neoptimizata)

    # l_closed contine nodurile expandate
    l_closed = []

    total_inlocuiti_open = 0
    total_inlocuiti_closed = 0
    while len(l_open) > 0:
        print("Open: " + str(l_open))
        print("Closed:"+str(l_closed))
        # print("Expandate: " + str(l_closed))
        nodCurent = l_open.pop(0)
        l_closed.append(nodCurent)
        if gr.testeaza_scop(nodCurent):
            print("Solutie: ", end="")
            nodCurent.afisDrum()
            print("\n----------------\n")
            # print("total inlocuite in open,", total_inlocuiti_open)
            # print("total inlocuite in closed,", total_inlocuiti_closed)
            return
        lSuccesori = gr.genereazaSuccesori(nodCurent)
        for s in lSuccesori:
            gasitC = False
            for nodC in l_open:
                if s.info == nodC.info:
                    gasitC = True
                    if s.f >= nodC.f:
                        lSuccesori.remove(s)
                    else:  # s.f<nodC.f
                        total_inlocuiti_open += 1
                        # print("se va inlocui ->",nodC,"din candidati cu",s,"care are un drum mai bun")
                        l_open.remove(nodC)
                    break

            if not gasitC:
                for nodC in l_closed:
                    if s.info == nodC.info:
                        if s.f >= nodC.f:
                            lSuccesori.remove(s)
                        else:  # s.f<nodC.f
                            total_inlocuiti_closed+=1
                            # print("se va inlocui -> ",nodC,"din expandate cu",s,"care are un drum mai bun")
                            l_closed.remove(nodC)
                        break
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(l_open)):
                # diferenta fata de UCS e ca ordonez crescator dupa f
                # daca f-urile sunt egale ordonez descrescator dupa g
                if l_open[i].f > s.f or (l_open[i].f == s.f and l_open[i].g <= s.g):
                    gasit_loc = True
                    break
            if gasit_loc:
                l_open.insert(i, s)
            else:
                l_open.append(s)

def a_star_megaOptimizat(gr):

    l_open = queue.PriorityQueue()
    l_open.put(NodParcurgere(gr.noduri.index(gr.start), gr.start, None, 0, gr.calculeaza_h(gr.start)))

    l_closed = {}

    while not l_open.empty():
        nodCurent = l_open.get()
        l_closed[nodCurent.id] = nodCurent

        if gr.testeaza_scop(nodCurent):
            print("Solutie: ", end="")
            nodCurent.afisDrum()
            print("\n----------------\n")
            return

        lSuccesori = gr.genereazaSuccesori(nodCurent)

        for s in lSuccesori:
            if s.id in l_closed:
                if l_closed[s.id] > s:
                    l_closed[s.id] = s

        for s in lSuccesori:
            l_open.put(s)




# 1,4,5 8,10 <---9			20
# (f=10,g=7)(f=14,g=3)    <----(f=10,g=3)
a_star(gr)
a_star_megaOptimizat(gr)

# cProfile.run("a_star(gr)")
# cProfile.run("a_star_megaOptimizat(gr)")