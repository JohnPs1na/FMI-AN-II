
factori :: Int -> [Int] 
factori n = [a | a <- [1..n],n `mod` a == 0]

prim :: Int -> Bool 
prim n = length (factori n) == 2

numerePrime :: Int -> [Int] 
numerePrime x = [a | a <- [2..x], prim a]

myzip3 :: [Int] -> [Int] -> [Int] -> [(Int,Int,Int)]
myzip3 xs ys zs = [(x,y,z) | (x,sx) <- xs `zip` [0..] ,((y,z),syz) <- (ys `zip` zs) `zip` [0..], sx == syz]

ordonataNat :: [Int] -> Bool 
ordonataNat [] = True 
ordonataNat [x] = True 
ordonataNat (x:xs) = and [a < b | (a,b) <- (x:xs) `zip` xs]

ordonataNat1 :: [Int] -> Bool 
ordonataNat1 [] = True 
ordonataNat1 [x] = True 
ordonataNat1 (x:xs) 
    | x < head xs = ordonataNat xs
    |otherwise = False


ordonata :: [a] -> (a->a->Bool) ->Bool 
ordonata (x:xs) op = and [op a b | (a,b) <- (x:xs) `zip` xs]

(*<*) :: (Integer,Integer) -> (Integer,Integer) -> Bool 
(*<*) a b = fst a < fst b && snd a < snd b
infix 6 *<*


compuneList :: (b->c) -> [(a->b)] -> [(a->c)]
compuneList f [] = [] 
compuneList f (x:xf) = f.x : compuneList f xf

aplicaList :: a -> [(a->b)] -> [b]
aplicaList x xf = [f x | f<-xf]
