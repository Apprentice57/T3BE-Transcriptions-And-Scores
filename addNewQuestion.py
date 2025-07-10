#!/usr/bin/env python3

import os, textwrap

question_dir = "question_texts"

for cur in sorted(os.listdir(question_dir)):
    if os.path.isfile(os.path.join(question_dir, cur)):
        last_entry = cur

with open(os.path.join(question_dir, last_entry), "rt", encoding="utf-8", newline="") as f:
    title = next(f).strip()

last_entry = last_entry[:-4]
next_entry = f"R{int(last_entry[1:])+1:03d}"

print(f"Last question: {last_entry}")
print(f"  Last title: {title}")
print(f"Next question: {next_entry}")

yn = input("Does this look right? [y/(n)] ")
if yn != "y":
    exit(1)

title = input("Title: ")
print("Question and answers: ('.' to end entry)")
question = []
while True:
    if len(question) > 2 and question[-1] == "" and question[-2] == "":
        break
    temp = input()
    if temp == ".":
        break
    question.append(temp)

while len(question) and question[-1] == "":
    question.pop(-1)

print("-" * 74)
print(title)
print("")
for row in question:
    if len(row) == 0:
        print("")
    else:
        for sub_row in textwrap.wrap(row, width=72, subsequent_indent="    "):
            print(sub_row)
print("-" * 74)

yn = input("Does this look right? [y/(n)] ")
if yn != "y":
    exit(1)

with open(os.path.join(question_dir, next_entry + ".txt"), "wt", newline="", encoding="utf-8") as f:
    f.write(title + "\n")
    f.write("\n")
    f.write("\n".join(question))
    f.write("\n")

for fn, skip_letter in (("AllQuestions.txt", False), ("OldQuestions.txt", False), ("RebootQuestions.txt", True)):
    with open(fn, "at", newline="", encoding="utf-8") as f:
        f.write("\n")
        f.write("Question #")
        f.write(next_entry[1:] if skip_letter else next_entry)
        f.write("\n")
        f.write(title + "\n")
        f.write("\n")
        f.write("\n".join(question))
        f.write("\n")

print("Done, updated files")
