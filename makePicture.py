import os, sys

import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# Inputs
file_path = "."
input_path = os.path.join(file_path,"lastTenResults.txt")
output_path = os.path.join(file_path, "lastTenResults.png")


# Read in results file
with open(input_path) as file:
    lines = [line.rstrip() for line in file]
# Grab Question numbers
idx = [lines.index(l) for l in lines if l.startswith("|    Username")]
username = lines.pop(idx[0])
question_num = str(username).split("|")[2:-3]
question_num = [num_str.replace(" ", "") for num_str in question_num]

# Grab correct answers
idx = [lines.index(l) for l in lines if l.startswith("|    Correct Answer")]
correct_ans = lines.pop(idx[0])
answers = str(correct_ans).split("|")[2:-3]
answers = [ans_str.replace(" ", "") for ans_str in answers]


# Grab Totals
idx = [lines.index(l) for l in lines if l.startswith("|        Total")]
total_line = lines.pop(idx[0])
total_line = str(total_line).split("|")[1:-1]
total_line = [temp_str.replace(" ", "") for temp_str in total_line]

# Prep df for user answers and scores
question_col = ["Question_" + s for s in question_num]
score_col = ["Score_" + s for s in question_num]
col_names = ["user"] + question_col + score_col + ["Last_10", "Total"]
user_scores = pd.DataFrame(columns=col_names)

# Loop through users building dataframe
for line in lines:
    line = str(line).split("|")

    # We should only have spacing lines and user names left so it is safe to
    # ignore split lines that are short
    if len(line) > 4:
        user_dict = {"user": line[1].replace(" ", "")}
        user_answer = line[2:-3]
        user_answer = [ans_str.replace(" ", "") for ans_str in user_answer]

        user_dict.update(
            {question_col[i]: user_answer[i] for i in range(len(question_col))}
        )
        user_dict.update(
            {
                score_col[i]: user_answer[i] == answers[i]
                for i in range(len(question_col))
            }
        )
        user_dict.update({"Last_10": line[-3].replace(" ", "")})
        user_dict.update({"Total": line[-2].replace(" ", "")})

        user_scores = pd.concat([user_scores, pd.DataFrame([user_dict])])

# Put dataframe into pretty table
table_columns = ["Username / Q#"] + question_num + ["Last 10", "Total"]
colors = []
cell_text = []
cell_text.append([""] * 13)
colors.append(["lightsteelblue"] * 13)
cell_text.append(["Correct Answer"] + answers + ["", ""])
colors.append(["w"] * 13)
cell_text.append([""] * 13)
colors.append(["w"] * 13)

for index, row in user_scores.iterrows():
    cell_text.append(
        row[["user"] + question_col + ["Last_10", "Total"]].values.flatten().tolist()
    )

    # Build color array based on scores
    row_color = ["w"]
    for n in range(0, len(score_col)):
        if row[score_col[n]]:
            row_color.append("forestgreen")
        elif (not row[score_col[n]]) and row[question_col[n]] != "":
            row_color.append("lightcoral")
        else:
            row_color.append("w")
    row_color.append("w")
    row_color.append("w")
    colors.append(row_color)

cell_text.append([""] * 13)
colors.append(["lightsteelblue"] * 13)
cell_text.append(total_line)
colors.append(["w"] * 13)

# Make Plot
fig, ax = plt.subplots()
ax.axis("tight")
ax.axis("off")

the_table = ax.table(
    cellText=cell_text,
    cellColours=colors,
    colLabels=table_columns,
    loc="center",
    colWidths=[0.5] + [0.2] * 12,
)

the_table.auto_set_font_size(True)
the_table.set_fontsize(13)
the_table.scale(1, 2)

for (row, col), cell in the_table.get_celld().items():
    if row == 0 or row == len(cell_text) or col == 0 or col == 11 or col == 12:
        cell.set_text_props(fontproperties=FontProperties(weight="bold"))

fig.savefig(output_path, bbox_inches="tight")

