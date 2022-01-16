import Data.List

type Name = String

data  Value  =  VBool Bool
     |VInt Int
     |VFun (Value -> Value)
     |VError

data  Hask  = HTrue | HFalse
     |HIf Hask Hask Hask
     |HLit Int
     |Hask :==: Hask
     |Hask :+:  Hask
     |HVar Name
     |HLam Name Hask
     |Hask :$: Hask

infix 4 :==:
infixl 6 :+:
infixl 9 :$:

type  HEnv  =  [(Name, Value)]


instance Show Value where
     show (VBool b) = show b
     show (VInt i) = show i
     show (VFun f) = "Error: Functions arent instances of show"
     show VError = "Error: Errors arent instances of show"

instance Eq Value where
    VBool x1 == VBool x2 = x1 == x2
    VInt x1 == VInt x2 = x1 == x2
    VBool x1 == _ = error "Cant compare boolean with non boolean"
    VInt x1 == _ = error "Cant compare Int with non Int"
    VFun f1 == _ = error "Cant compare functions"
    VError == _ = error "cant compare errors"

hEval :: Hask -> HEnv -> Value
hEval HTrue r      =  VBool True
hEval HFalse r        =  VBool False
hEval (HIf c d e) r   = hif (hEval c r) (hEval d r) (hEval e r)
  where  hif (VBool b) v w  =  if b then v else w
         hif _ _ _ = VError

hEval (HLit x) xs = VInt x
hEval (HVar x) xs = myLookUp x xs
hEval (HLam x e) xs = VFun(\fx -> hEval e ((x,fx):xs))

hEval (x :==: y) xs
    |hEval x xs == hEval y xs = VBool True
    |hEval x xs /= hEval y xs = VBool False
    | otherwise = error "Cant Compare different datatypes"

hEval (x:+:y) xs = addHask (hEval x xs) (hEval y xs)
    where
        addHask (VInt a) (VInt b) = VInt (a + b)
        addHask _ _ = error "Cant add 2 different things"

hEval (x:$:y) xs = hLam (hEval x xs) (hEval y xs)
    where
        hLam (VFun f) a = f a
        hLam _ _ = error "Invalid Lambda arguments"

myLookUp::Name -> HEnv -> Value
myLookUp n [] = error "Value not found"
myLookUp n ((k,v):xs)
    |n == k = v
    |otherwise = myLookUp n xs

run :: Hask -> String
run pg = show (hEval pg [])
