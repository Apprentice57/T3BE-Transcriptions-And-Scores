import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
import numpy as np

# Inputs
file_path = r"."
last_10_path = os.path.join(file_path, "lastTenResults.txt")
all_path = os.path.join(file_path, "allResults.txt")
output_path = os.path.join(file_path, "lastTenResults.png")

hot_map = mcolors.LinearSegmentedColormap.from_list("hotStreak", ["lightgreen", "limegreen","green","darkgreen"], 5)
cold_map = mcolors.LinearSegmentedColormap.from_list("coldStreak", ["lightcoral","tomato","red","darkred"], 5)
score_map = mcolors.LinearSegmentedColormap.from_list("scoreMap", ["red","yellow","green"], 10)

font_color = mcolors.to_hex('gainsboro')
font_type = "DejaVu Sans" #Matt sends his deepest dissapointment "Garamond"
fig_color = "#282814"
title_cell_hex = "#3c3c50"
answer_color = mcolors.to_hex('black')
user_color = ["#242a2d", "#3c3c3c"]

def main():
    # Read in answer files
    with open(all_path) as file:
        all_lines = [line.rstrip() for line in file]

    with open(last_10_path) as file:
        last_10_lines = [line.rstrip() for line in file]

    # Get question/answers for entire set
    question_num, answers = get_q_and_a(all_lines)
    total_line = get_totals(last_10_lines)

    # Grab user names who have been active in the last 10
    users, last_10, all_scores = get_user_names(last_10_lines)
    
    # Create Pretty Table
    # Put dataframe into pretty table
    table_columns = ["Username / Q#"] + question_num[-10:] + ["Last 10", "Total"]
    colors = []
    cell_text = []
    cell_text.append(["Correct Answer"] + answers[-10:] + ["", ""])
    colors.append([title_cell_hex] * 13)

    # Create user score dataframe
    for nUser in range(0,len(users)):
        user_score = score_user(all_lines, users[nUser], answers)
        cell_text.append([users[nUser]] + user_score.Answer[-10:].to_list() + [last_10[nUser], all_scores[nUser]])
        
        # Build color array based on streaks
        row_color = [user_color[nUser % 2]]
        for nScore in range(len(user_score)-10,len(user_score)):
            if pd.isna(user_score.Score[nScore]):
                cell_color = user_color[nUser % 2]
            elif user_score.Score[nScore]:
                cell_color = mcolors.to_hex(hot_map(int(user_score.Hot_Streak[nScore])))
            elif (not user_score.Score[nScore]):
                cell_color = mcolors.to_hex(cold_map(int(user_score.Cold_Streak[nScore])))
            row_color.append(cell_color)

        row_color.append(user_color[nUser % 2])
        row_color.append(user_color[nUser % 2])
        colors.append(row_color)
                
    totals = total_line[-12:]
    totals.insert(0,total_line[0])
    cell_text.append(totals)
    
    row_color = [title_cell_hex]
    for nScore in range(1,len(totals)-2):
        int_list = [int(s) for s in totals[nScore].split("/")]
        percent = np.floor(int_list[0]/int_list[1]*10)
        row_color.append(mcolors.to_hex( score_map(int(percent))))
    row_color.append(title_cell_hex)
    row_color.append(title_cell_hex)
    colors.append(row_color)
    
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
    
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(12)
    the_table.scale(1, 2)
    
    
    for i, col_name in enumerate(table_columns): 
        cell = the_table.get_celld()[(0, i)]
        cell.set_text_props(weight='bold',color=font_color)
        cell.set_fontsize(16)
        cell.set_facecolor(title_cell_hex)
        
        cell = the_table.get_celld()[(len(cell_text), i)]
        cell.set_fontsize(16)


    
    for (row, col), cell in the_table.get_celld().items():  
        cell.set_text_props(weight='bold',ha='center',va='center',fontname=font_type)
        #Set font color for answers
        if row > 1 and col != 0 and col != 11 and col != 12:
            cell.set_text_props(color=answer_color)
        else:
            cell.set_text_props(color=font_color)

            
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)



def get_q_and_a(lines):
    # Grab Question numbers
    idx = [lines.index(l) for l in lines if l.startswith("|    Username")]
    username = lines[idx[0]]
    question_num = str(username).split("|")[2:-3]
    question_num = [num_str.replace(" ", "") for num_str in question_num]

    # Grab correct answers
    idx = [
        lines.index(l) for l in lines if l.startswith("|    Correct Answer")
    ]
    correct_ans = lines[idx[0]]
    answers = str(correct_ans).split("|")[2:-3]
    answers = [ans_str.replace(" ", "") for ans_str in answers]

    return question_num, answers


def get_totals(lines):
    # Grab Totals
    idx = [lines.index(l) for l in lines if l.startswith("|        Total")]
    total_line = lines[idx[0]]
    total_line = str(total_line).split("|")[1:-1]
    total_line = [temp_str.replace(" ", "") for temp_str in total_line]

    return total_line


def get_user_names(lines):
    users = []
    last_10 = []
    all_scores = []
    for line in lines:
        line = str(line).split("|")
        # Ignore lines that don't split
        if len(line) > 4:
            user_name = line[1].replace(" ", "")
            if user_name not in ["Username/Q#->", "CorrectAnswer", "Total:"]:
                users.append(user_name)
                last_10.append(line[-3].replace(" ", ""))
                all_scores.append(line[-2].replace(" ", ""))
            
    return users, last_10, all_scores


def score_user(lines, user, answers):
    for line in lines:
        line = str(line).split("|")
        # Ignore lines that don't split
        if len(line) > 4:
            user_name = line[1].replace(" ", "")
            if user_name == user:
                #Create user dataframe
                user_answer = [ans_str.replace(" ", "") for ans_str in line[2:-3]]
                user_dict = {"Answer": user_answer}
                score = [a == b for a, b in zip(user_answer, answers)]
                user_dict.update({"Score": score})
                user_score = pd.DataFrame.from_dict(user_dict)
                
                user_score['Score'] = user_score['Score'].astype('object')
                user_score.loc[user_score['Answer'] == '', 'Score'] = pd.NA

                #Calculate Hot and Cold Streaks
                user_score["Hot_Streak"] = (
                    user_score.groupby(
                        (user_score["Score"]& ~user_score["Score"].shift(1).fillna(False).infer_objects(copy=False)).cumsum()
                    )
                    .cumcount()
                    .add(1)
                    * user_score["Score"]
                )
                
                user_score['inverted_Score'] = ~user_score['Score'].astype('boolean')
                user_score["Cold_Streak"] = (
                    user_score.groupby(
                        (user_score["inverted_Score"]& ~user_score["inverted_Score"].shift(1).fillna(False).infer_objects(copy=False)).cumsum()
                    )
                    .cumcount()
                    .add(1)
                    * user_score["inverted_Score"]
                )
                
    return user_score


if __name__ == "__main__":
    main()
