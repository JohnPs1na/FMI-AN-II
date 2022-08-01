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

t = int(input())

for i in range(t):
    x = input().split()
    p = [int(j) for j in x[:2]]
    q = [int(j) for j in x[2:4]]
    r = [int(j) for j in x[4:]]

    print(tokyoDrift(p,q,r))