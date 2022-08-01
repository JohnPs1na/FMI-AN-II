def getSum(xs,k):
    dp = [[0 for i in range(k+1)] for j in range(len(xs)+1)]

    for i in range(1,len(xs)+1):
        for j in range(k+1):
            if xs[i-1] > j:
                dp[i][j] = dp[i-1][j]
            else:
                dp[i][j] = max(dp[i-1][j],dp[i-1][j-xs[i-1]] + xs[i-1])

    for i in dp:
        print(i)
    return dp[len(xs)][k]

def getSumGreedy():
    res = 0
    suma = 0

    with open('../input.in') as f:
        k = int(f.readline())
        i = f.readline()
        while i:
            i = int(i)
            if i <= k:
                suma += i
                k -= i
            res = max(res,i)
            i = f.readline()

    return max(res,suma)

weight = 50

print(getSumGreedy())