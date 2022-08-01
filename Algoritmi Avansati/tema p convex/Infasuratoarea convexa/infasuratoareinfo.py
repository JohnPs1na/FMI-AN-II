def calc_det(points, q, r):
    det = q[0] * r[1] + points[1] * r[0] + points[0] * q[1] - points[1] * q[0] - points[0] * r[1] - r[0] * q[1]
    return det

n = int(input())

points = []
mini = [2e9,'*']
for i in range(n):
    points.append([int(j) for j in input().split()])
    if points[i][0] <= mini[0]:
        mini = points[i]


index = points.index(mini)
l = index
result = [mini]
while True:
    q = (l + 1) % len(points)
    for i in range(len(points)):
        if i == l:
            continue
        d = calc_det(points[l], points[i], points[q])
        if d < 0:
            q = i
    l = q
    if l == index:
        break
    result.append(points[q])

result = result[::-1]
print(len(result))
for i in result:
    print(i[0], i[1])
