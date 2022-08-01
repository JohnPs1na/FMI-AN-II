import random
import time


class Elev:
    default_i = 1

    def __init__(self, nume="", l_activitati=None, sanatate=90, inteligenta=20, oboseala=0, buna_dispozitie=100):

        if l_activitati is None:
            l_activitati = []

        if nume == '':
            nume = "Necunoscut_" + str(Elev.default_i)
            Elev.default_i += 1
        self.nume = nume
        self.sanatate = sanatate
        self.inteligenta = inteligenta
        self.oboseala = oboseala
        self.buna_dispozitie = buna_dispozitie
        self.activitate_curenta = None
        self.timp_executat_activitate = {}
        for i in lista_activitati:
            self.timp_executat_activitate[i.nume] = 0

    def desfasoara_activitate(self, activitate):
        self.activitate_curenta = activitate

    def trece_ora(self, Ora):

        self.timp_executat_activitate[self.activitate_curenta.nume] += 1
        self.sanatate = max(min(100,
                            self.sanatate + self.activitate_curenta.factor_sanatate),0)
        self.inteligenta = max(min(100,
                               self.inteligenta + self.activitate_curenta.factor_inteligenta),0)
        self.oboseala = max(min(100,
                            self.oboseala + self.activitate_curenta.factor_oboseala),0)
        self.buna_dispozitie = max(min(100,
                                   self.buna_dispozitie + self.activitate_curenta.factor_dispozitie),0)

        if 22 < Ora < 6 and self.activitate_curenta.nume != 'dormit':
            self.sanatate -= 1

        if self.timp_executat_activitate[self.activitate_curenta.nume] == self.activitate_curenta.durata:
            self.timp_executat_activitate[self.activitate_curenta.nume] = 0
            self.activitate_curenta = lista_activitati[random.randint(0,len(lista_activitati)-1)]
            return False

        return True

    def testeaza_final(self):
        if self.inteligenta == 100 or self.sanatate == 0 or self.buna_dispozitie == 0:
            return True
        return False

    def afiseaza_raport(self):
        sir = self.nume + '\n'
        for i in self.timp_executat_activitate:
            sir += (i + ':' + str(self.timp_executat_activitate[i]) + '\n')

        return sir

    def __repr__(self):
        sir = self.nume + ', '
        sir += 'act ' + self.activitate_curenta.nume + ' ('
        sir += ('hp ' + str(self.sanatate)) + ', '
        sir += ('smort ' + str(self.inteligenta)) + ', '
        sir += ('obos ' + str(self.oboseala)) + ', '
        sir += ('gud ' + str(self.buna_dispozitie)) + ') '
        return sir


class Activitate:
    def __init__(self, nume, factor_sanatate, factor_inteligenta, factor_oboseala, factor_dispozitie, durata):
        self.nume = nume
        self.factor_sanatate = factor_sanatate
        self.factor_inteligenta = factor_inteligenta
        self.factor_oboseala = factor_oboseala
        self.factor_dispozitie = factor_dispozitie
        self.durata = durata

    def __repr__(self):
        sir = self.nume + ':\n'
        sir += ('factor_sanatate - ' + str(self.factor_sanatate) + '\n')
        sir += ('factor_inteligenta - ' + str(self.factor_inteligenta) + '\n')
        sir += ('factor_oboseala - ' + str(self.factor_oboseala) + '\n')
        sir += ('factor_dispozitie - ' + str(self.factor_dispozitie) + '\n')
        sir += ('durata - ' + str(self.durata) + '\n')
        return sir


def porneste_simulare(ls_elevi):
    ora = 9
    while True:
        for i in ls_elevi:
            print(i)
        comanda = input()

        if comanda == 'gata':
            break

        finalizeaza = 0
        if comanda == 'continua':
            finalizeaza = 1
            while ls_elevi:
                for elev in ls_elevi:
                    if elev.activitate_curenta is None:
                        elev.activitate_curenta = lista_activitati[random.randint(0,len(lista_activitati)-1)]
                    elev.trece_ora(ora)
                ora += 1

                for elev in ls_elevi:
                    if elev.testeaza_final():
                        print(elev)
                        if elev.inteligenta >= 100:
                            print("elevul a sfarsit scoala")
                        if elev.sanatate <= 0 or elev.oboseala >= 100:
                            print("elevul a ajuns in spital")
                        ls_elevi.remove(elev)

        elif comanda.isnumeric():
            num = int(comanda)
            print(num)
            for i in range(num):
                for elev in ls_elevi:
                    a = elev.activitate_curenta.nume

                    if not elev.trece_ora(ora):
                        print(elev.nume, 'a terminat de', a)
                    print(elev.afiseaza_raport())
                ora += 1
                time.sleep(1)

        if finalizeaza == 1:
            print("Sfarsit Simulare")
            break


if __name__ == "__main__":

    with open('data.in') as f:

        lista_factori = f.readline().split()[1:]

        dict_activitati = {}
        lista_activitati = []
        x = f.readline().split()
        while x:
            dict_activitati[x[0]] = [int(i) for i in x[1:]]
            lista_activitati.append(Activitate(x[0], *[int(i) for i in x[1:]]))
            x = f.readline().split()

    Ionel = Elev('Ionel')
    Gigel = Elev('Gigel')
    Simona = Elev('Simona')

    lista_elevi = [Ionel, Gigel, Simona]

    for i in range(len(lista_elevi)):
        lista_elevi[i].activitate_curenta = lista_activitati[random.randint(0, len(lista_elevi) - 1)]
    porneste_simulare(lista_elevi)
