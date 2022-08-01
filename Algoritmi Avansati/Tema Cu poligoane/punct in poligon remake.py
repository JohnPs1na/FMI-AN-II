# check if q lies on [p r]
def onSegment(p, q, r):
    if max(p[0], r[0]) >= q[0] >= min(p[0], r[0]) and max(p[1], r[1]) >= q[1] >= min(p[1], r[1]):
        return True
    return False


def orientation(p, q, r):
    val = q[0]*r[1] + p[0]*q[1] + p[1]*r[0] - q[0]*p[1] - r[0]*q[1] - r[1]*p[0]

    if val == 0:
        return 0  # colinear
    if val > 0:
        return 'da'
    else:
        return 'nu'


def intersect(a, b, c, d):
    o1 = orientation(a, b, c)
    o2 = orientation(a, b, d)
    o3 = orientation(c, d, a)
    o4 = orientation(c, d, b)

    if o1 == 0 and onSegment(a, c, b):
        return 2

    if o1 != o2 and o3 != o4:
        return 1

    return 0


n = int(input())
points = []
edges = []

for i in range(n):

    px, py = [int(j) for j in input().split()]

    points.append((px, py))

    if i > 0:
        edges.append((points[i - 1], points[i]))

edges.append((points[len(points) - 1], points[0]))

num_of_points = int(input())

m = (2e11+32414,2e11+38048)

for i in range(num_of_points):

    point = [int(i) for i in input().split()]

    ok = 0
    counter = 0
    for edge in edges:
        rez = intersect(edge[0], edge[1], point, m)
        if rez == 1:
            counter += 1

        if rez == 2:
            print("BOUNDARY")
            ok = 1
            break

    if not ok:
        if counter % 2 == 1:
            print("INSIDE")
        else:
            print("OUTSIDE")
