import argparse

import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", default="./data/so_python_10000.csv", type=str, help="Path to the csv file")


# Count the number of questions which have accepted answers
def count_accepted_answers(df):
    df = df.drop_duplicates('q_id')
    count = sum(df["q_accepted_answer_id"].notna())
    print(f"Number of questions w/ accepted answers: {count} / {len(df)}")

# Count the number of answers with code sample
def count_answers_w_code(df):
    count =  sum(["<code>" in answer for answer in df["a_body"]])
    print(f"Number of answers w/ code: {count} / {len(df)}")


def main():
    args = parser.parse_args()
    df = pd.read_csv(args.input)
    count_accepted_answers(df)
    count_answers_w_code(df)

if __name__ == "__main__":
    main()