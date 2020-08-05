#!/usr/bin/env scriptisto

-- scriptisto-begin
-- script_src: script.hs
-- build_cmd: ghc -O -o script script.hs && strip ./script
-- scriptisto-end

import Data.List
import Data.List.Split
import System.Environment

-- Zips 2 lists into one
zip' :: [a]->[a]->[a]
zip' _ [] = []
zip' [] _ = []
zip' (x:xs) (y:ys) = [x, y] ++ (zip' xs ys)

{- 
 - Spreads a range of Int so that each element is as far apart from their 
 - neighbor as possible.
 -}
spread :: Int -> [Int]
spread 1 = [0]
spread n = do
    let m = (div n 2)
    let list = spread m
    nub ([n-1] ++ (zip' list (map (+m) list))) -- Creates an distinct

-- Mapping spread function to list elements 
spreadList :: [a] -> [a]
spreadList list = (map (list !!) (spread (length list))) 

main = do 
    args <- getArgs
    if length args == 0
        then do
            contents <- getContents 
	    putStrLn (intercalate "\n" (spreadList (lines contents)))
    else putStrLn (intercalate "\n" (spreadList args))

