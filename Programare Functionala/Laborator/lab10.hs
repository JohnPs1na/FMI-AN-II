import Data.Maybe

data Expr = Const Int -- integer constant
          | Expr :+: Expr -- addition
          | Expr :*: Expr -- multiplication
           deriving Eq

data Operation = Add | Mult deriving (Eq, Show)

data Tree = Lf Int -- leaf
          | Node Operation Tree Tree -- branch
           deriving (Eq, Show)


instance Show Expr where
    show (Const a) = show a
    show (a :+: b) = show a ++ "+" ++ show b
    show (a :*: b) = show a ++ "*" ++ show b



evalExp :: Expr -> Int
evalExp (Const a) = a
evalExp (a :+: b) = evalExp a + evalExp b
evalExp (a :*: b) = evalExp a * evalExp b

exp1 = ((Const 2 :*: Const 3) :+: (Const 0 :*: Const 5))
exp2 = (Const 2 :*: (Const 3 :+: Const 4))
exp3 = (Const 4 :+: (Const 3 :*: Const 3))
exp4 = (((Const 1 :*: Const 2) :*: (Const 3 :+: Const 1)) :*: Const 2)
test11 = evalExp exp1 == 6
test12 = evalExp exp2 == 14
test13 = evalExp exp3 == 13
test14 = evalExp exp4 == 16

evalArb :: Tree -> Int
evalArb (Lf x) = x
evalArb (Node Add l r ) = evalArb l + evalArb r
evalArb (Node Mult l r) = evalArb l * evalArb r


expToArb :: Expr -> Tree
expToArb (Const a) = Lf a
expToArb (e1 :+: e2) = Node Add (expToArb e1) (expToArb e2)
expToArb (e1 :*: e2) = Node Mult (expToArb e1) (expToArb e2)

arb1 = Node Add (Node Mult (Lf 2) (Lf 3)) (Node Mult (Lf 0)(Lf 5))
arb2 = Node Mult (Lf 2) (Node Add (Lf 3)(Lf 4))
arb3 = Node Add (Lf 4) (Node Mult (Lf 3)(Lf 3))
arb4 = Node Mult (Node Mult (Node Mult (Lf 1) (Lf 2)) (Node Add (Lf 3)(Lf 1))) (Lf 2)

test21 = evalArb arb1 == 6
test22 = evalArb arb2 == 14
test23 = evalArb arb3 == 13
test24 = evalArb arb4 == 16

class Collection c where
  empty :: c key value
  singleton :: key -> value -> c key value
  insert
      :: Ord key
      => key -> value -> c key value -> c key value
  clookup :: Ord key => key -> c key value -> Maybe value
  delete :: Ord key => key -> c key value -> c key value
  keys :: c key value -> [key]
  keys c = [k | (k,v) <- toList c]
  values :: c key value -> [value]
  values c = [v | (k,v) <- toList c]
  toList :: c key value -> [(key, value)]
  fromList :: Ord key => [(key,value)] -> c key value
  fromList xs = foldr (uncurry insert) empty xs

newtype PairList k v
  = PairList { getPairList :: [(k, v)] }


--nu am idee daca am facut corect
instance Collection PairList where
    empty = PairList []
    singleton k v = PairList [(k,v)]
    insert k v c = PairList (getPairList c ++ [(k,v)])
    clookup _ (PairList []) = Nothing
    clookup k c = lookup k (getPairList c)
    delete x (PairList xs) =PairList [(k,v) | (k,v) <- xs, k /= x]
    toList c = getPairList c



data SearchTree key value
  = Empty
  | BNode
      (SearchTree key value) -- elemente cu cheia mai mica
      key                    -- cheia elementului
      (Maybe value)          -- valoarea elementului
      (SearchTree key value) -- elemente cu cheia mai mare

instance Collection SearchTree where 
    empty = Empty 
    singleton k v = BNode Empty k (Just v) Empty
    insert k v Empty = singleton k v 
    insert k v (BNode l key value r)
        | k < key = BNode (insert k v l) key value r
        | k > key = BNode l key value (insert k v l)
        | k == key = BNode l key (Just v) r

    clookup _ Empty = Nothing 
    clookup k (BNode l key value r) 
        | k == key = value 
        | k > key = clookup k r 
        | k < key = clookup k l 

    delete k (BNode l key value r)
        | k == key = BNode l key Nothing r 
        | k < key = BNode (delete k l) key value r 
        | k > key = BNode l key value (delete k r )

    toList Empty = [] 
    toList (BNode l _ Nothing r) = toList l ++ toList r 
    toList (BNode l k (Just v) r) = toList l ++ [(k,v)] ++ toList r
