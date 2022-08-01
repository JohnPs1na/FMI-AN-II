def tokyoDrift(p, q, r):
    det = q[0]*r[1] + p[0]*q[1] + p[1]*r[0] - q[0]*p[1] - r[0]*q[1] - r[1]*p[0]

    if det < 0:
        return -1  # la dreapta

    return 1  # stanga / colinear


n = int(input())
points = []
for i in range(n):
    points.append([float(x) for x in input().split()])


def cmp(xs):
    return xs[0], xs[1]


def getInf(xs):
    stek = [xs[0], xs[1]]
    for i in range(2, len(xs)):
        point = xs[i]
        while len(stek) > 1 and tokyoDrift(stek[-2], stek[-1], point) < 0:
            stek.pop()
        stek.append(point)
    return stek

jos = getInf(points)

reversedPoints = points[::-1]
sus = getInf(reversedPoints)

convexHull = jos
for i in sus:
    if i not in convexHull:
        convexHull.append(i)

print(str(len(convexHull)))
for i in convexHull:
    print(str(int(i[0])) + ' ' + str(int(i[1])))
