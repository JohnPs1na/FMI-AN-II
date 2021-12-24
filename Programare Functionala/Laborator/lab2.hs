

poly2 :: Double -> Double -> Double -> Double -> Double
poly2 a b c x = a*(x*x) + b*x + c

eeny :: Int -> String 
eeny a 
    | even a = "eeny"
    |otherwise = "meeny"

fizzBuzz :: Int -> String 
fizzBuzz x = 
    if x `mod` 15 == 0 then "FizzBuzz"
    else if x `mod` 5 == 0 then "Buzz"
    else if x `mod` 3 == 0 then "Fizz"
    else ""

fizzbuzz :: Int -> String 
fizzbuzz x 
    | x `mod` 15 == 0 = "FizzBuzz"
    | x `mod` 5 == 0 = "Buzz"
    | x `mod` 3 == 0 = "Fizz"
    |otherwise = ""

tribonacci :: Int -> Int 
tribonacci n
    | n <= 2 = 1
    | n == 3 = 2
    | n > 3 = tribonacci (n-1) + tribonacci(n-2) + tribonacci(n-3)

tribonacciEcuational :: Int -> Int
tribonacciEcuational 1 = 1
tribonacciEcuational 2 = 1
tribonacciEcuational 3 = 2
tribonacciEcuational a = tribonacciEcuational(a-1) + tribonacciEcuational(a-2) + tribonacciEcuational(a-3)

binomial :: Int->Int->Int
binomial a 0 = 1
binomial 0 b = 0
binomial n k = binomial (n-1) k + binomial (n-1) (k-1)

verifL :: [Int] -> Bool 
verifL xs = even (length  xs)

takefinal :: [Int] -> Int -> [Int]
takefinal xs n 
    |length xs < n = xs
    | otherwise = reverse (take n (reverse xs))


remove :: [Int] -> Int -> [Int]
remove xs n = take (n-1) xs ++ drop n xs 


myReplicate :: Int -> Int -> [Int]
myReplicate 0 v = []
myReplicate n v = v : myReplicate (n-1) v

sumImp :: [Int] -> Int
sumImp [] = 0
sumImp (x:xs)
    | even x = sumImp xs
    | otherwise = x + sumImp xs

totalLen :: [String] -> Int
totalLen [] = 0
totalLen (x:xs)
    | head x == 'A' = length x + totalLen xs
    | otherwise = totalLen xs
