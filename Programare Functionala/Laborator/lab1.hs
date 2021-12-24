--lab 1
double :: Integer -> Integer 
double x = x+x

maxim :: Int -> Int -> Int
maxim a b = 
    if a > b then a
    else b

maxim3 :: Int -> Int -> Int -> Int
maxim3 a b c = 
    if a >= b && a >= c then a
    else if b>=a && b>=c then b 
    else c


newMaxim3 :: Int -> Int -> Int -> Int
newMaxim3 x y z =
    let
        u = maxim x y
    in
        maxim u z

maxim4 :: Int -> Int -> Int -> Int -> Int 
maxim4 a b c d =
    let u = maxim3 a b c 
    in maxim u d

sumSquare :: Int->Int->Int
sumSquare a b = a*a + b*b

parityChecker :: Int -> String 
parityChecker a 
    | a `mod` 2 == 1 = "Impar"
    | otherwise  = "Par"

factorial :: Int -> Int
factorial 1 = 1
factorial a = a * factorial (a-1)

verif :: Int -> Int -> Bool 
verif a b 
    | a > b*2 = True 
    | otherwise = False
