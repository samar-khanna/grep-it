import argparse

import pandas as pd
import matplotlib.pyplot as plt 
parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", default="./so_rust.csv", type=str, help="Path to the csv file")


# Count the number of questions which have accepted answers
def count_accepted_answers(df):
    df = df.drop_duplicates('q_id')
    count = sum(df["q_accepted_answer_id"].notna())
    print(f"Number of questions w/ accepted answers: {count} / {len(df)}")

# Plot the histogram of answer count for questions
def hist_answer_count(df):
    df = df.drop_duplicates('q_id')
    vc = df["q_answer_count"].value_counts()
    median = df["q_answer_count"].median()
    print(f"Median number of answers to questions: {median}")
    vc.plot(kind='bar')
    plt.title("Count of different Answers to a Question on StackOverflow")
    plt.xlabel("Count of Questions")
    plt.ylabel("Count of different Answers")
    plt.savefig("./plots/so_hist_count_answers_to_questions.png")

# Count the number of answers with code sample
def count_answers_w_code(df):
    count =  sum(["<code>" in answer for answer in df["a_body"]])
    print(f"Number of answers w/ code: {count} / {len(df)}")

def main(parser=parser):
    args = parser.parse_args()
    df = pd.read_csv(args.input)
    count_accepted_answers(df)
    count_answers_w_code(df)
    hist_answer_count(df)

if __name__ == "__main__":
    main()