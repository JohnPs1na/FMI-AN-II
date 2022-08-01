def tokyoDrift1(p,q,r):
    def dete(a):
        return (a[0][0] * (a[1][1] * a[2][2] - a[2][1] * a[1][2])
                - a[1][0] * (a[0][1] * a[2][2] - a[2][1] * a[0][2])
                + a[2][0] * (a[0][1] * a[1][2] - a[1][1] * a[0][2]))
    xs = [[1,1,1],[p[0],q[0],r[0]],[p[1],q[1],r[1]]]

    det = dete(xs)

    if det > 0:
        return 1
    if det < 0:
        return -1
    return 0

def tokyoDrift(p, q, r):
    def dete(a):
        return (a[0][0] * (a[1][1] * a[2][2] - a[2][1] * a[1][2])
                - a[1][0] * (a[0][1] * a[2][2] - a[2][1] * a[0][2])
                + a[2][0] * (a[0][1] * a[1][2] - a[1][1] * a[0][2]))

    xs = [[1, 1, 1], [p[0], q[0], r[0]], [p[1], q[1], r[1]]]

    det = dete(xs)

    if det < 0:
        return -1  # la dreapta

    return 1  # stanga / colinear


with open('infasuratoare.in') as f:
    n = int(f.readline())

    points = []

    for i in range(n):
        points.append([float(x) for x in f.readline().split()])


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


points.sort(key=cmp)
jos = getInf(points)

reversedPoints = points[::-1]
sus = getInf(reversedPoints)

convexHull = jos
for i in sus:
    if i not in convexHull:
        convexHull.append(i)

myPoint = [float(i) for i in input().split()][:2]

for i in range(len(convexHull) - 1):
    p1 = convexHull[i]
    p2 = convexHull[i+1]

    if tokyoDrift1(p1,p2,myPoint) < 0:
        print("INSIDE")
        exit()

    elif tokyoDrift1(p1,myPoint,p2) == 0:
        print('OUTSIDE')
        exit()

print("BOUNDARY")