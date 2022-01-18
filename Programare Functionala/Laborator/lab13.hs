import Data.Monoid
import Data.Semigroup

elems :: (Foldable t, Eq a) => a -> t a -> Bool
elems x  = getAny . foldMap (Any . (==x))

nullc :: (Foldable t) => t a -> Bool
--nullc = foldr (\_ _ -> False) True
nullc  = getAll . foldMap (All . const False)

mylength :: (Foldable t) => t a -> Int
--mylength = foldr(\x acc -> acc+1) 0
mylength = getSum . foldMap (Sum . const 1)

toList :: (Foldable t) => t a -> [a]
--toList = foldr (:) []
toList = foldMap (: [])

fold :: (Foldable t, Monoid m) => t m -> m
fold = foldMap id

data Constant a b = Constant b
instance Foldable (Constant a) where
    foldMap f (Constant x) = f x

data Two a b = Two a b
instance Foldable (Two a) where
    foldMap f (Two a b) = f b

data Three a b c = Three a b c
instance Foldable (Three a b ) where
    foldMap f (Three a b c) = f c

data Three' a b = Three' a b b
instance Foldable (Three' a) where
    foldMap f (Three' x y z) = (f y) <> (f z)

data Four' a b = Four' a b b b
instance Foldable (Four' a) where
    foldMap f (Four' x y z t) = (f y) <> (f z) <> (f t)

data GoatLord a = NoGoat | OneGoat a | MoreGoats (GoatLord a) (GoatLord a) (GoatLord a)
instance Foldable GoatLord where
    foldMap f NoGoat = mempty
    foldMap f (OneGoat a) = f a
    foldMap f (MoreGoats g1 g2 g3) = foldMap f g1 <> foldMap f g2 <> (foldMap f g3)
