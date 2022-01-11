
import Data.Char
import Data.List


-- 1.
rotate :: Int -> [Char] -> [Char]
rotate x ls 
    | x > length ls = error "Nr prea mare"
    | x < 0 = error "Nr negativ"
    | otherwise = drop x ls ++ take x ls

-- 2.
prop_rotate :: Int -> String -> Bool
prop_rotate k str = rotate (l - m) (rotate m str) == str
                        where l = length str
                              m = if l == 0 then 0 else k `mod` l

-- 3.
makeKey :: Int -> [(Char, Char)]
makeKey x = ['A'..'Z'] `zip` rotate x ['A'..'Z']

-- 4.
lookUp :: Char -> [(Char, Char)] -> Char
lookUp e [] = e 
lookUp e (x:xs) 
    | e == fst x = snd x 
    | otherwise = lookUp e xs

-- 5.
encipher :: Int -> Char -> Char
encipher x c = lookUp c $ makeKey x

-- 6.
normalize :: String -> String
normalize [] = []
normalize (x:xs)
    | elem x ['a'..'z'] || elem x ['A'..'Z'] = toUpper x : normalize xs
    | elem x ['1'..'9'] = x : normalize xs
    | otherwise = normalize xs

-- 7.
encipherStr :: Int -> String -> String
encipherStr x st = [encipher x a | a <- normalize st]

-- 8.
reverseKey :: [(Char, Char)] -> [(Char, Char)]
reverseKey xs = [(b,a) | (a,b) <- xs]

-- 9.
decipher :: Int -> Char -> Char
decipher x c = lookUp c $ reverseKey (makeKey x)

decipherStr :: Int -> String -> String
decipherStr x st = [decipher x a | a <- normalize st]
