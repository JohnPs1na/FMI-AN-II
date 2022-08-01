def tokyoDrift1(p, q, r):
    def dete(a):
        return (a[0][0] * (a[1][1] * a[2][2] - a[2][1] * a[1][2])
                - a[1][0] * (a[0][1] * a[2][2] - a[2][1] * a[0][2])
                + a[2][0] * (a[0][1] * a[1][2] - a[1][1] * a[0][2]))

    xs = [[1, 1, 1], [p[0], q[0], r[0]], [p[1], q[1], r[1]]]

    det = dete(xs)

    if det < 0:
        return -1  # la dreapta
    elif det > 0:
        return 1  # la stanga
    return 0


def getPointPos(convexHull, myPoint):
    for i in range(len(convexHull) - 1):
        p1 = convexHull[i]
        p2 = convexHull[i + 1]

        if tokyoDrift1(p1, p2, myPoint) > 0:
            continue

        elif tokyoDrift1(p1, p2, myPoint) < 0:
            return 'OUTSIDE'

        elif tokyoDrift1(p1, p2, myPoint) == 0:
            return 'BOUNDARY'

    p1 = convexHull[-1]
    p2 = convexHull[0]

    if tokyoDrift1(p1,p2,myPoint) < 0:
        return "OUTSIDE"

    elif tokyoDrift1(p1,p2,myPoint) == 0:
        return "BOUNDARY"

    return "INSIDE"


t = int(input())

points = []
for i in range(t):
    points.append([int(j) for j in input().split()])

res = []

ps = int(input())

for i in range(ps):
    ps = [int(j) for j in input().split()]
    res.append(getPointPos(points, ps))


for i in res:
    print(i)