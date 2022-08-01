def determinantOfMatrix(mat):

    def getcofactor(m, i, j):
        return [row[: j] + row[j + 1:] for row in (m[: i] + m[i + 1:])]

    if (len(mat) == 2):
        value = mat[0][0] * mat[1][1] - mat[1][0] * mat[0][1]
        return value

    Sum = 0
    for current_column in range(len(mat)):
        sign = (-1) ** (current_column)
        sub_det = determinantOfMatrix(getcofactor(mat, 0, current_column))
        Sum += (sign * mat[0][current_column] * sub_det)

    return Sum


matrix1 = [[1 for i in range(4)] for j in range(4)]
matrix2 = [[1 for i in range(4)] for j in range(4)]

patrulater = []

for i in range(4):
    px, py = [int(j) for j in input().split()]
    patrulater.append((px,py))

    matrix1[i][0] = px
    matrix1[i][1] = py
    matrix1[i][2] = px*px + py*py

    if i > 0:
        matrix2[i-1][0] = px
        matrix2[i-1][1] = py
        matrix2[i-1][2] = px*px + py*py

matrix2[3][0] = patrulater[0][0]
matrix2[3][1] = patrulater[0][1]
matrix2[3][2] = patrulater[0][0]**2 + patrulater[0][1]**2

deter1 = determinantOfMatrix(matrix1)
deter2 = determinantOfMatrix(matrix2)

if deter1 > 0:
    print("AC: ILLEGAL")
else:
    print("AC: LEGAL")

if deter2 > 0:
    print("BD: ILLEGAL")
else:
    print("BD: LEGAL")
