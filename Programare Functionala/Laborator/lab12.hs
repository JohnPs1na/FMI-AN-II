import Data.Functor

newtype Identity a = Identity a
    deriving (Show, Eq)

instance Functor Identity where 
    fmap f (Identity a) = Identity (f a)

x = Identity 5
data Pair a = Pair a a
    deriving (Show, Eq)

instance Functor Pair where
    fmap f (Pair x y) = Pair (f x) (f y)

data Constant a b = Constant b
    deriving (Show, Eq)

instance Functor (Constant a) where 
    fmap f (Constant x) = Constant (f x)

data Two a b = Two a b
    deriving (Show, Eq)

instance Functor (Two a) where 
    fmap f (Two a b) = Two a (f b)

data Three a b c = Three a b c
    deriving (Show, Eq)

instance Functor (Three a b) where 
    fmap f (Three a b c) = Three a b (f c)

data Three' a b = Three' a b b
    deriving (Show, Eq)

instance Functor (Three' a) where 
    fmap f (Three' x y z) = Three' x (f y) (f z)


data Four a b c d = Four a b c d
    deriving (Show, Eq)

instance Functor (Four a b c) where 
    fmap f (Four x y z t) = Four x y z (f t)

data Four'' a b = Four'' a a a b
    deriving (Show, Eq)

instance Functor (Four'' a) where
    fmap f (Four'' x y z t) = Four'' x y z (f t)

data Quant a b = Finance | Desk a | Bloor b
    deriving (Show, Eq)

instance Functor (Quant a) where
    fmap f Finance = Finance
    fmap f (Desk a) = Desk a
    fmap f (Bloor b) = Bloor (f b)


data LiftItOut f a = LiftItOut (f a)
    deriving (Show, Eq)

instance Functor f => Functor (LiftItOut f) where 
    fmap f (LiftItOut x) = LiftItOut (fmap f x)

data Parappa f g a = DaWrappa (f a) (g a)
    deriving (Show, Eq)

instance (Functor f,Functor g) => Functor (Parappa f g) where
    fmap f (DaWrappa fx fg) = DaWrappa (fmap f fx) (fmap f fg)


data IgnoreOne f g a b = IgnoringSomething (f a) (g b)
    deriving (Show, Eq)

instance (Functor g) => Functor (IgnoreOne f g a) where 
    fmap f (IgnoringSomething fx fy) = IgnoringSomething fx (fmap f fy)

data Notorious g o a t = Notorious (g o) (g a) (g t)
    deriving (Show, Eq)

instance (Functor g) => Functor (Notorious g o a) where 
    fmap f (Notorious gf go ga) = Notorious gf go (fmap f ga)

data GoatLord a = NoGoat | OneGoat a | MoreGoats (GoatLord a) (GoatLord a) (GoatLord a)
    deriving (Show)


instance Functor GoatLord where 
    fmap f NoGoat = NoGoat 
    fmap f (OneGoat a) = OneGoat (f a)
    fmap f (MoreGoats g1 g2 g3) = MoreGoats (fmap f g1) (fmap f g2) (fmap f g3)

data TalkToMe a = Halt | Print String a | Read (String -> a)

instance Functor TalkToMe where 
    fmap f Halt = Halt 
    fmap f (Print s x) = Print s (f x)
    fmap f (Read g) = Read (f.g)
