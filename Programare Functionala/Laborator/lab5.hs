firstEl :: [(a,b)] -> [a]
firstEl = map fst

sumList :: [[Int]] -> [Int]
sumList = map sum

pre12 :: [Int] -> [Int]
pre12 = map fun
    where fun x = if even x then x `div` 2 else x*2

verifC :: Char -> [[Char]] -> [[Char]]
verifC x = filter (elem x)

squareOdds :: [Int] -> [Int]
squareOdds xs= map (^2)$filter odd xs

numaiVocale :: [[Char]] -> [[Char]]
numaiVocale xs = map decatVocale xs
    where
        decatVocale [] = []
        decatVocale (x:xs) = if elem x "aeiouAEIOU" then x : decatVocale xs else decatVocale xs

--nu le-am testat
mymap :: (a->b) -> [a] -> [b]
mymap f [] =[]
mymap f (x:xs) = f x : mymap f xs

myfilter :: (a->Bool) -> [a] -> [a]
myfilter f [] = []
myfilter f (x:xs)
    | f x = x : myfilter f xs
    | otherwise = myfilter f xs

sumOddsSquares :: [Int] -> Int
sumOddsSquares xs = sum (squareOdds xs)

verifTrue :: [Bool] -> Bool
verifTrue = foldr (&&) True

rmChar :: Char -> String -> String 
rmChar x st = filter (/= x) st

rmCharsRec :: String -> String -> String 
rmCharsRec [] st2 = st2 
rmCharsRec (x:st1) (st2) = rmCharsRec st1 (rmChar x st2)

rmCharsFoldr :: String -> String -> String 
rmCharsFoldr st1 st2 = foldr rmChar st2 st1  
