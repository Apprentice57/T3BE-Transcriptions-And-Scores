#!/bin/bash

numQuestions=$(find ./answers -type f -name "*.txt" | wc -l)

rm lastTenResults.txt
rm allResults.txt

python3 tabulateT3BEResults.py 10 2 > lastTenResults.txt
python3 tabulateT3BEResults.py "$numQuestions" 1 > allResults.txt

python3 makePicture.py

current_date=$(date +"%Y_%m_%d")
directory="./scores/$current_date"
mkdir -p "$directory"

cp lastTenResults.png "$directory"
cp lastTenResults.txt "$directory"
cp allResults.txt "$directory"

