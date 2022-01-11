import Data.Maybe
data Fruct = Mar String Bool | Portocala String Int

ionatanFaraVierme = Mar "Ionatan" False
goldenCuVierme = Mar "Golden Delicious" True
portocalaSicilia10 = Portocala "Sanguinello" 10
listaFructe = [Mar "Ionatan" False,
                Portocala "Sanguinello" 10,
                Portocala "Valencia" 22,
                Mar "Golden Delicious" True,
                Portocala "Sanguinello" 15,
                Portocala "Moro" 12,
                Portocala "Tarocco" 3,
                Portocala "Moro" 12,
                Portocala "Valencia" 2,
                Mar "Golden Delicious" False,
                Mar "Golden" False,
                Mar "Golden" True]

ePortocalaDeSicilia :: Fruct -> Bool
ePortocalaDeSicilia (Mar _ _)= False
ePortocalaDeSicilia (Portocala x _)
    | x == "Tarocco" || x == "Moro" || x == "Sanguinello" = True
    | otherwise = False

nrFeliiSicilia :: [Fruct] -> Int
nrFeliiSicilia xs = sum [b | (Portocala a b) <- xs, ePortocalaDeSicilia (Portocala a b)]

nrMereViermi :: [Fruct] -> Int
nrMereViermi xs = sum [1 | (Mar _ b) <- xs, b]


type NumeA = String
type Rasa = String
data Animal = Pisica NumeA | Caine NumeA Rasa
    deriving Show

vorbeste :: Animal -> String
vorbeste (Pisica _) = "Meow!"
vorbeste (Caine _ _) = "Woof!"

rasa :: Animal -> Maybe String
rasa (Pisica _) = Nothing
rasa (Caine _ x) = Just x

data Linie = L [Int]
    deriving Show
data Matrice = M [Linie]
    deriving Show


verifica :: Matrice -> Int -> Bool
verifica (M xs) n = length (filter ((==n) . sumaLinie) xs) == length xs
    where
        sumaLinie (L ls) = sum ls


doarPozN :: Matrice -> Int -> Bool
doarPozN (M xs) n = and [verifPozitive l | l <-xs, lun l == n]
    where
        verifPozitive (L ls) = and [x>=0 | x<-ls]
        lun (L ls) = length ls


corect :: Matrice -> Bool
corect (M xs) = lunMat (M xs) == length (filter (\(L xs) -> length xs==n) xs)
    where
        lun (L ls) = length ls
        n = lun (head xs)
        lunMat (M xs) = sum [1 | (L _) <- xs]
