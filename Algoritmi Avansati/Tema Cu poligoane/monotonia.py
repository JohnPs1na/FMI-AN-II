n = int(input())

maxy_idy = -1
maxy = -2e7

maxx_idy = -1
maxx = -2e7

points = []
for i in range(n):
    px, py = [int(j) for j in input().split()]

    if py > maxy:
        maxy = py
        maxy_idy = i

    if px > maxx:
        maxx = px
        maxx_idy = i

    points.append((px, py))

ys = points[maxy_idy:] + points[:maxy_idy] + [points[maxy_idy]]
xs = points[maxx_idy:] + points[:maxx_idy] + [points[maxx_idy]]

idx = 0
initialx = maxx
okx = 0
while maxx >= xs[idx][0]:
    maxx = xs[idx][0]
    idx += 1

idx -= 1

while maxx <= xs[idx][0]:
    if initialx == xs[idx][0] and len(xs) - 1 == idx:
        okx = 1
        break
    maxx = xs[idx][0]
    idx += 1

if okx:
    print("YES")
else:
    print("NO")

idy = 0
initialy = maxy
oky = 0

while maxy >= ys[idy][1]:
    maxy = ys[idy][1]
    idy += 1

idy -= 1

while maxy <= ys[idy][1]:
    if initialy == ys[idy][1] and len(ys) - 1 == idy:
        oky = 1
        break
    maxy = ys[idy][1]
    idy += 1

if oky:
    print("YES")
else:
    print("NO")