import Data.Char

getVocale::String -> Int
getVocale [] = 0
getVocale (x:xs)
    | x `elem` "aeiou" = 1 + getVocale xs
    |otherwise = getVocale xs

nrVocale :: [String] -> Int
nrVocale [] = 0
nrVocale (x:xs)
    | x == reverse x = getVocale x + nrVocale xs
    | otherwise = nrVocale xs


intAfterEven :: Int -> [Int] -> [Int]
intAfterEven x [] = []
intAfterEven x (h:xs)
    | even h = h : x : intAfterEven x xs
    | otherwise = h : intAfterEven x xs

divisors :: Int -> [Int]
divisors x = [a | a <- [1..x], x `mod` a == 0]

divisorList :: [Int] -> [[Int]]
divisorList xs = [divisors x | x <- xs]

inInterval :: Int -> Int -> [Int] -> [Int]
inInterval inf sup xs = [x | x <- xs, x>=inf, x<=sup]

inIntervalRec :: Int -> Int -> [Int] -> [Int] 
inIntervalRec inf sup [] = []
inIntervalRec inf sup (x:xs)
    | x >= inf && x <= sup = x : inIntervalRec inf sup xs 
    |otherwise = inIntervalRec inf sup xs 


positivesRec :: [Int] -> Int 
positivesRec [] = 0
positivesRec (x:xs) 
    | x >= 0 = 1 + positivesRec xs 
    |otherwise = positivesRec xs 

positivesComp :: [Int] -> Int 
positivesComp xs = sum [x `div` x | x<-xs, x >= 0]

oddPositionsComp :: [Int] -> [Int]
oddPositionsComp xs = [b | (a,b) <- xs `zip` [0..], odd a]

oddPositionsRec :: [Int] -> [Int]
oddPositionsRec xs = getWithIndexes 0 xs
    where 
        getWithIndexes idx [] = []
        getWithIndexes idx (x:xs) 
            | odd x = idx : getWithIndexes (idx+1) xs
            | otherwise = getWithIndexes (idx+1) xs

multDigitsRec :: String -> Int 
multDigitsRec [] = 1 
multDigitsRec (x : ls) 
    | isDigit x = digitToInt x * multDigitsRec ls
    | otherwise = multDigitsRec ls

multDigitsComp :: String -> Int 
multDigitsComp ls = product [digitToInt x | x <- ls, isDigit x]
