def tokyoDrift(p, q, r):
    def dete(a):
        return (a[0][0] * (a[1][1] * a[2][2] - a[2][1] * a[1][2])
                - a[1][0] * (a[0][1] * a[2][2] - a[2][1] * a[0][2])
                + a[2][0] * (a[0][1] * a[1][2] - a[1][1] * a[0][2]))

    xs = [[1, 1, 1], [p[0], q[0], r[0]], [p[1], q[1], r[1]]]

    det = dete(xs)

    if det > 0:
        return "LEFT"
    if det < 0:
        return 'RIGHT'
    return 'TOUCH'


def cmp(xs):
    return xs[0]


# check if q lies on pr
def checkOnline(p, r, q):
    if max(p[0], r[0]) >= q[0] >= min(p[0], r[0]) and\
            max(p[1], r[1]) >= q[1] >= min(p[1], r[1]):
        return True
    return False


def intersect(bigSeg, smolSeg):
    a = bigSeg[0]
    b = bigSeg[1]
    c = smolSeg[0]
    d = smolSeg[1]

    r1 = tokyoDrift(a, b, c)
    r2 = tokyoDrift(a, b, d)

    v1 = tokyoDrift(c, d, a)
    v2 = tokyoDrift(c, d, b)

    if r1 != r2 and v1 != v2:
        return True

    return False


m = (2e7, 2e7)

n = int(input())
points = []
edges = []

for i in range(n):

    px, py = [int(j) for j in input().split()]

    points.append((px, py))

    if i > 0:
        edges.append((points[i - 1], points[i]))

edges.append((points[len(points) - 1], points[0]))

p = int(input())

for i in range(p):
    point = [int(j) for j in input().split()]
    my_segment = [point, m]

    counter = 0
    ok = 0
    for edge in edges:
        if checkOnline(edge[0], edge[1], point):
            print("BOUNDARY")
            ok = 1
            break

        if intersect(my_segment, edge):
            counter += 1

    if ok:
        continue

    if counter % 2:
        print("INSIDE")
    else:
        print("OUTSIDE")
