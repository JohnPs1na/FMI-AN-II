def determinantOfMatrix(mat):

    def getcofactor(m, i, j):
        return [row[: j] + row[j + 1:] for row in (m[: i] + m[i + 1:])]
    # if given matrix is of order
    # 2*2 then simply return det
    # value by cross multiplying
    # elements of matrix.
    if (len(mat) == 2):
        value = mat[0][0] * mat[1][1] - mat[1][0] * mat[0][1]
        return value

    # initialize Sum to zero
    Sum = 0

    # loop to traverse each column
    # of matrix a.
    for current_column in range(len(mat)):
        # calculating the sign corresponding
        # to co-factor of that sub matrix.
        sign = (-1) ** (current_column)

        # calling the function recursily to
        # get determinant value of
        # sub matrix obtained.
        sub_det = determinantOfMatrix(getcofactor(mat, 0, current_column))

        # adding the calculated determinant
        # value of particular column
        # matrix to total Sum.
        Sum += (sign * mat[0][current_column] * sub_det)

    # returning the final Sum
    return Sum


matrix = [[1 for i in range(4)] for j in range(4)]

for i in range(3):
    tx,ty = [int(i) for i in input().split()]
    matrix[i][0] = tx
    matrix[i][1] = ty
    matrix[i][2] = tx*tx+ty*ty

lastPoint = 3
points = int(input())

for i in range(points):
    px, py = [int(i) for i in input().split()]
    matrix[lastPoint][0] = px
    matrix[lastPoint][1] = py
    matrix[lastPoint][2] = px*px + py*py

    determ = determinantOfMatrix(matrix)

    if determ == 0:
        print("BOUNDARY")
    if determ > 0:
        print("INSIDE")
    if determ < 0:
        print("OUTSIDE")

