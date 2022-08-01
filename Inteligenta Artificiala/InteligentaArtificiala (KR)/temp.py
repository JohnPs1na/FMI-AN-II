def plusMinus(arr):
    d = [0,0,0]
    n = len(arr)
    for i in arr:
        if i > 0:
            d[2]+=1
        if i == 0:
            d[1] += 1
        if i < 0:
            d[0] += 1
    print(d[2]/n)
    print(d[1]/n)
    print(d[0]/n)

plusMinus([1,1,0,-1,-1])