#!/bin/bash

#Merge Old Question Texts
concatenated_text=""
# Merge question wording together with added question prefix
for file in question_texts/*.txt; do
    firstchar=$(basename "$file" | cut -c 1-2)

    if [[ ${firstchar} != "R" ]];then
        prefix=$(basename "$file" | cut -c 1-4)
        concatenated_text+="Question #$prefix\n"
        concatenated_text+=$(cat "$file")
        concatenated_text+="\n\n"
    fi
done

rm OldQuestions.txt
echo "$concatenated_text" > OldQuestions.txt

#Merge New Question Texts
concatenated_text=""
for file in question_texts/R*.txt; do
    prefix=$(basename "$file" | cut -c 2-4)
    concatenated_text+="Question #$prefix\n"
    concatenated_text+=$(cat "$file")
    concatenated_text+="\n\n"
done

rm RebootQuestions.txt
echo "$concatenated_text" > RebootQuestions.txt

#Merge All Question Texts
concatenated_text=""
# Merge question wording together with added question prefix
for file in question_texts/*.txt; do
    prefix=$(basename "$file" | cut -c 1-4)
    concatenated_text+="Question #$prefix\n"
    concatenated_text+=$(cat "$file")
    concatenated_text+="\n\n"
done

rm AllQuestions.txt
echo "$concatenated_text" > AllQuestions.txt

