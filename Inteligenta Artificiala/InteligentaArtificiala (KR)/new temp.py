def cauta(xs):
    n = len(xs) + 1

    total = n*(n+1) // 2

    for i in xs:
        total -= i

    return total

def cautxor(xs):
    n = len(xs) + 1
    elem = 0
    for i in range(1,n+1):
        elem^=i

    for i in xs:
        elem^=i

    return elem


def quicksort(xs):
    if len(xs) <= 1:
        return xs
    pivot = xs[0]

    Left = [i for i in xs if i < pivot]
    Right = [i for i in xs if i > pivot]
    Mid = [i for i in xs if i == pivot]

    return quicksort(Left) + Mid + quicksort(Right)

xs = [2134,21,34,99,12,2332]

sored = quicksort(xs)

print(sored)