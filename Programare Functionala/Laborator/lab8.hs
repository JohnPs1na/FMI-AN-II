import Data.Maybe
import Data.List

type Nume = String
data Prop
    = Var Nume
    | F
    | T
    | Not Prop
    | Prop :|: Prop
    | Prop :&: Prop
    | Prop :<->: Prop
    | Prop :->: Prop
    deriving (Eq)
infixr 2 :|:
infixr 3 :&:

p1 :: Prop
p1 = (Var "P" :|: Var "Q") :&: (Var "P" :&: Var "Q")

p2 :: Prop
p2 = (Var "P" :|: Var "Q") :&: (Not (Var "P") :&: Not (Var "Q"))

p3 :: Prop
p3 = (Var "P" :&: (Var "Q" :|: Var "R")) :&: ((Not (Var "P") :|: Not (Var "Q")) :&: (Not (Var "P") :|: Not (Var "R")))


instance Show Prop where
    show (Var nume) = nume
    show F = "F"
    show T = "T"
    show (Not p) = "(~"++ show p ++ ")"
    show ( a :|: b ) = "(S"++show a ++ "|" ++ show b++")"
    show ( a :&: b ) = "("++show a ++ "&" ++ show b++")"
    show ( a :->: b ) = "("++show a ++ "->" ++ show b++")"
    show ( a :<->: b ) = "("++show a ++ "<->" ++ show b++")"

test_ShowProp :: Bool
test_ShowProp = show (Not (Var "P") :&: Var "Q") == "((~P)&Q)"

type Env = [(Nume, Bool)]

impureLookup :: Eq a => a -> [(a,b)] -> b
impureLookup a = fromJust . lookup a

eval :: Prop -> Env -> Bool
eval F e = False
eval T e = True
eval (Var n) e = impureLookup n e
eval (Not p) e = not (eval p e)
eval (a :&: b) e = eval a e && eval b e
eval (a :|: b) e = eval a e || eval b e
eval (a :->: b) e = eval (Not a) e || eval b e
eval (a :<->: b) e = (eval (Not a) e || eval b e) && (eval (Not b) e || eval a e)




test_eval = eval  (Var "P" :|: Var "Q") [("P", True), ("Q", False)]

variabile :: Prop -> [Nume]
variabile F = []
variabile T = []
variabile (Var n) = [n]
variabile (Not p) = variabile p
variabile (a :|: b) = nub (variabile a ++ variabile b)
variabile (a :&: b) = nub (variabile a ++ variabile b)
variabile (a :->: b) = nub (variabile a ++ variabile b)
variabile (a :<->: b) = nub (variabile a ++ variabile b)



test_variabile =
  variabile (Not (Var "P") :&: Var "Q") == ["P", "Q"]

envs :: [Nume] -> [Env]
envs [] = [[]]
envs (n:nume) = [(n,False) : e | e <- envs nume] ++ [(n,True) : e | e <- envs nume]

test_envs =
    envs ["P", "Q"]
    ==
    [ [ ("P",False)
      , ("Q",False)
      ]
    , [ ("P",False)
      , ("Q",True)
      ]
    , [ ("P",True)
      , ("Q",False)
      ]
    , [ ("P",True)
      , ("Q",True)
      ]
    ]


satisfiabila :: Prop -> Bool
satisfiabila x = or [eval x e | e <- envs (variabile x)]


test_satisfiabila1 = satisfiabila (Not (Var "P") :&: Var "Q") == True
test_satisfiabila2 = satisfiabila (Not (Var "P") :&: Var "P") == False

valida :: Prop -> Bool
valida x = not (satisfiabila (Not x))

test_valida1 = valida (Not (Var "P") :&: Var "Q") == False
test_valida2 = valida (Not (Var "P") :|: Var "P") == True


echivalenta :: Prop -> Prop -> Bool
echivalenta p1 p2 = and [eval (p1 :<->: p2) a | a <- (envs (variabile (p1 :<->: p2)))]

test_echivalenta1 =
  True
  ==
  (Var "P" :&: Var "Q") `echivalenta` (Not (Not (Var "P") :|: Not (Var "Q")))
test_echivalenta2 =
  False
  ==
  (Var "P") `echivalenta` (Var "Q")
test_echivalenta3 =
  True
  ==
  (Var "R" :|: Not (Var "R")) `echivalenta` (Var "Q" :|: Not (Var "Q"))
