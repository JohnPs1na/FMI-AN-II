import copy
import math
import random

def myBin(x):
    global chromosomeLen
    st = bin(x)[2:]
    while len(st) < chromosomeLen:
        st = '0' + st
    return st
data = {}

dim = 'Dimension'
domain = 'Domain'
factors = 'Factors'
precision = 'Precision'
crossOverProb = 'Cross Over Probability'
mutationProb = 'Mutation Probability'
maxSteps = 'Steps'

g = open('output','w')
g.write('EVOLUTION\n\nFirst Population: \n')

with open('input') as f:
    data[dim] = int(f.readline())
    data[domain] = [float(i) for i in f.readline().split()]
    data[factors] = [float(i) for i in f.readline().split()]
    data[precision] = int(f.readline())
    data[crossOverProb] = float(f.readline())
    data[mutationProb] = float(f.readline())
    data[maxSteps] = int(f.readline())

interval = (data[domain][1] - data[domain][0]) * (10 ** data[precision])  # how much of x'es can be

chromosomeLen = math.ceil(math.log2(math.ceil(interval)))
maxNum = (2 ** chromosomeLen) - 1

# randomly create the very first population
Population = [random.randint(0, 2 ** chromosomeLen - 1) for i in range(data[dim])]


def fitness(num):
    return data[factors][0] * (num ** 2) + data[factors][1] * num + data[factors][2]


def getNum(chromosome):
    global data
    numba = chromosome / maxNum
    numba *= (data[domain][1] - data[domain][0])
    numba += data[domain][0]
    numba = round(numba, data[precision])
    return numba


def binaryInsert(xs, target):
    lo = 0
    hi = len(xs) - 1

    while lo <= hi:
        mid = lo + (hi - lo) // 2

        if target == xs[mid]:
            return mid
        elif target > xs[mid]:
            lo = mid + 1
        else:
            hi = mid - 1

    return lo


# initialize the elite guy
elite = [1, fitness(getNum(Population[0])), Population[0], getNum(Population[0])]

for iteration in range(data[maxSteps]):

    totalFitness = 0
    sel_probabilities = [0] * data[dim]

    infoPopulation = []

    for idx, chromosome in enumerate(Population):
        numba = getNum(chromosome)

        # get info about our population
        f = fitness(numba)
        infoPopulation.append([idx, numba, f, chromosome])

        if iteration == 0:
            g.write(f'{idx+1}:\t {bin(chromosome)[2:]}.\t x = {numba},\t f = {f}\n')

        # get the elite guy
        if f > elite[1]:
            elite = [idx, f, chromosome,numba]

        totalFitness += f

    #elita e deja gata

    if iteration == 0:
        g.write('\nSelection Probabilities:\n')
        g.write(f'chromosome: {0 + 1}: Probability : {infoPopulation[0][2] / totalFitness}\n')
    sel_probabilities[0] = infoPopulation[0][2] / totalFitness

    # get the probabilities of chromosomes to be selected for contributing to future populations
    for i in range(1, data[dim]):
        if iteration == 0:
            g.write(f'chromosome: {i + 1}: Probability : {infoPopulation[i][2] / totalFitness}\n')
        sel_probabilities[i] = (infoPopulation[i][2] / totalFitness) + sel_probabilities[i - 1]

    if iteration == 0:
        g.write('\nProbabilities Intervals:\n')
        for i in sel_probabilities:
            g.write(f'{round(i,5)} ')

    selected = [infoPopulation[elite[0]]]

    if iteration == 0:
        g.write(f'\n\nSelecting the Chromosomes\n')

    # randomly select chromosomes for the next population
    while len(selected) != data[dim]:
        numba = random.uniform(0, 1)
        sel = copy.deepcopy(infoPopulation[binaryInsert(sel_probabilities, numba)])
        if iteration == 0:
            g.write(f'u = {numba}\t select chromosome number {sel[0]}\n')

        sel[0] = len(selected)
        selected.append(sel)

    selected[0][0] = 0
    if iteration == 0:
        g.write(f'\nChromosomes after selection:\n')
        for chrom in selected:
            g.write(f'{chrom[0] + 1}: {bin(chrom[3])[2:]} \t x = {chrom[1]} \t f = {chrom[2]}\n')

    afterCrossing = [infoPopulation[elite[0]][3]]
    # get the guys who will combine
    crossingOver = []
    if iteration == 0:
        g.write(f'\nSelecting chromosomes for crossing over:\n')

    for specimen in selected:
        numba = random.uniform(0, 1)
        if numba <= data[crossOverProb]:
            if iteration == 0:
                g.write(f'{specimen[0] + 1}: \t{bin(specimen[3])[2:]} \t u = {numba} <= {data[crossOverProb]}, participates \n')
            crossingOver.append(specimen)
        else:
            if iteration == 0:
                g.write(f'{specimen[0] + 1}: \t{bin(specimen[3])[2:]} \t u = {numba}\n')
            afterCrossing.append(specimen[3])

    if iteration == 0:
        g.write('\nRecombinations:\n')

    for i in range(0, len(crossingOver) - 1, 2):

        male = myBin(Population[crossingOver[i][0]])
        female = myBin(Population[crossingOver[i + 1][0]])
        randomPoint = random.randint(0, chromosomeLen)

        if iteration == 0:
            g.write(f'p1 = {male}\t p2 = {female}\t Point at {randomPoint}\n')

        # y = myBin(male >> randomPoint)
        # x = myBin(female & (2 ** randomPoint - 1))
        #
        # y1 = myBin(male & (2 ** randomPoint - 1))
        # x1 = myBin(female >> randomPoint)
        #
        # print(myBin(male),myBin(female))
        # print(myBin(y),myBin(y1),myBin(x1),myBin(x))

        # child1 = int(bin(y)[2:] + bin(x)[2:], 2)
        # child2 = int(bin(x1)[2:] + bin(y1)[2:], 2)

        y = male[:randomPoint]
        y1 = male[randomPoint:]
        x = female[randomPoint:]
        x1 = female[:randomPoint]

        child1 = int(y + x, 2)
        child2 = int(x1 + y1, 2)

        if iteration == 0:
            g.write('Children: ')
            g.write(f'c1 = {bin(child1)[2:]}\t c2 = {bin(child2)[2:]}\n')

        afterCrossing.append(child1)
        afterCrossing.append(child2)

    while len(afterCrossing) > 20:
        afterCrossing.pop()

    if iteration == 0:
        g.write('\nAfter CrossingOver:\n')
        for i in range(len(afterCrossing)):
            x = getNum(afterCrossing[i])
            g.write(f'{i+1}: {bin(afterCrossing[i])[2:]},\t x = {x},\t f = {fitness(x)}\n')

    if iteration == 0:
        g.write('\nMutation Process:\n')

    afterMutating = [elite[2]]
    for idx,specimen in enumerate(afterCrossing):
        for prob in range(chromosomeLen):
            numba = random.uniform(0, 1)
            if numba < data[mutationProb]:
                specimen ^= 1 << prob
                if iteration == 0:
                    g.write(f'Has Mutated chromosome {idx + 1}\n')
                break
        while specimen > interval:
            specimen >>= 1

        afterMutating.append(specimen)

    if iteration == 0:
        g.write('\nChromosomes after Mutation:\n')
        for i in range(len(afterMutating)):
            x = getNum(afterMutating[i])
            g.write(f'{i + 1}: {bin(afterMutating[i])[2:]},\t x = {x},\t f = {fitness(x)}\n')

    Population = afterMutating

    if iteration == 0:
        g.write("\nEvolution of maximum:\n")

    g.write(str(elite[1]) + '\n')


    # [idx, numar, cromo, fitness]
