#!/bin/bash

numQuestions=$(find ./answers -type f -name "*.txt" | wc -l)

rm lastTenResults.txt
rm allResults.txt

python3 tabulateT3BEResults.py 10 > lastTenResults.txt
python3 tabulateT3BEResults.py "$numQuestions" > allResults.txt

