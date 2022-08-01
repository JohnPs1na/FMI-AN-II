def tokyoDrift(p,q,r):
    def dete(a):
        return (a[0][0] * (a[1][1] * a[2][2] - a[2][1] * a[1][2])
                - a[1][0] * (a[0][1] * a[2][2] - a[2][1] * a[0][2])
                + a[2][0] * (a[0][1] * a[1][2] - a[1][1] * a[0][2]))
    xs = [[1,1,1],[p[0],q[0],r[0]],[p[1],q[1],r[1]]]

    det = dete(xs)

    if det > 0:
        return "LEFT"
    if det < 0:
        return 'RIGHT'
    return 'TOUCH'

res = [0,0,0]
t = int(input())

points = []
for i in range(t):
    points.append([int(j) for j in input().split()])
    if len(points) >= 3:
        p = points[i-2]
        q = points[i-1]
        r = points[i]

        if tokyoDrift(p,q,r) == "LEFT":
            res[0]+=1
        elif tokyoDrift(p,q,r) == "RIGHT":
            res[1]+=1
        else:
            res[2]+=1

p = points[-2]
q = points[-1]
r = points[0]

if tokyoDrift(p, q, r) == "LEFT":
    res[0] += 1
elif tokyoDrift(p, q, r) == "RIGHT":
    res[1] += 1
else:
    res[2] += 1

print(res[0],res[1],res[2])