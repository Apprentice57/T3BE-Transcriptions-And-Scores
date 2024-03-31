#!/bin/bash

# Initialize an empty variable to store concatenated text
concatenated_text=""

# Loop through each .txt file in the current directory
for file in individualtxtfiles/*.txt; do
    # Extract the first three characters of the filename
    prefix=$(basename "$file" | cut -c 1-3)
    # Add "Question XXX" followed by a newline to the concatenated text
    concatenated_text+="Question #$prefix\n"
    # Append the contents of the file to the concatenated text
    concatenated_text+=$(cat "$file")
    # Add an extra newline for separation between files
    concatenated_text+="\n\n"
done

rm AllQuestions.txt

# Print the concatenated text
echo "$concatenated_text" > AllQuestions.txt


