n = int(input())

planes = []

for i in range(n):
     planes.append([int(x) for x in input().split()])

#a mai mare ca 0 -> in stanga
#a mai mic ca 0 -> in dreapta
maxiStangaA = 2e9
miniDreaptaA = -2e9

maxiJosB = 2e9
miniSusB = -2e9

for plane in planes:
    if plane[1] == 0:
        proportion = -plane[2]/plane[0]
        if plane[0] < 0:
            miniDreaptaA = max(proportion,miniDreaptaA)
        if plane[0] > 0:
            maxiStangaA = min(proportion,maxiStangaA)
    if plane[0] == 0:
        proportion = -plane[2]/plane[1]
        if plane[1] < 0:
            miniSusB = max(miniSusB,proportion)
        if plane[1] > 0:
            maxiJosB = min(maxiJosB,proportion)

if maxiStangaA < miniDreaptaA or maxiJosB < miniSusB:
    print("VOID")
elif maxiStangaA != 2e9 and miniDreaptaA != -2e9 and miniSusB != -2e9 and maxiJosB != 2e9:
    print("BOUNDED")
else:
    print("UNBOUNDED")
