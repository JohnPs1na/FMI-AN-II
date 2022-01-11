sfChr :: Char -> Bool 
sfChr x = x `elem` ".!?:"

nrSentences :: String -> Int
nrSentences [] = 0 
nrSentences (x:xs)
    |sfChr x = 1 + nrSentences xs 
    |otherwise = nrSentences xs 

nrSen :: String -> Int 
nrSen xs = sum [1 | x <- xs, sfChr x]

liniiN :: [[Int]] -> Int -> Bool 
liniiN mat n = and [strictPoz x | x <- mat, (length x) == n]
    where 
        strictPoz x = and [a >= 0 | a<-x]


data Punct = Pt [Int]
    deriving Show

data Arb = Vid | F Int | N Arb Arb
    deriving Show

class ToFromArb a where
    toArb :: a -> Arb
    fromArb :: Arb -> a


instance ToFromArb Punct where
    toArb (Pt []) = Vid
    toArb (Pt (x:xs)) = N (F x) (toArb (Pt xs))

    fromArb Vid = Pt [] 
    fromArb (F x) = Pt [x] 
    fromArb (N l r) = add (fromArb l) (fromArb r)
        where 
            add (Pt x) (Pt y) = Pt (x++y)
