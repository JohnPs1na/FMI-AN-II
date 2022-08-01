n = int(input())
planes = []

for i in range(n):
    planes.append([int(i) for i in input().split()])

def getIntersections(planes,point):
    maxiStangaA = 2e9
    miniDreaptaA = -2e9
    maxiJosB = 2e9
    miniSusB = -2e9

    for plane in planes:
        if plane[0] == 0:
            proportion = -plane[2]/plane[1]
            if plane[1]*point[1] + plane[2] >= 0:
                continue
            if proportion < point[1]:
                miniSusB = max(miniSusB,proportion)
            else:
                maxiJosB = min(maxiJosB,proportion)
        elif plane[1] == 0:
            proportion = -plane[2]/plane[0]
            if plane[0] * point[0] + plane[2] >= 0:
                continue
            if proportion < point[0]:
                miniDreaptaA = max(miniDreaptaA,proportion)
            else:
                maxiStangaA = min(maxiStangaA,proportion)

    if min(miniDreaptaA,miniSusB) == -2e9 or max(maxiStangaA,maxiJosB) == 2e9:
        return 0
    else:
        return (maxiStangaA - miniDreaptaA) * (maxiJosB - miniSusB)


m = int(input())

for i in range(m):
    point = [float(x) for x in input().split()]
    x = getIntersections(planes,point)
    if x:
        print("YES")
        print(x)
    else:
        print("NO")