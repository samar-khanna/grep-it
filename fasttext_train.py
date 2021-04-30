import os
import argparse
import fasttext
import pandas as pd
from tokenizers import Tokenizer
from data.rust_tokenizer import train_tokenizer


def passed_arguments():
    parser = argparse.ArgumentParser(description="Script to train fasttext skipgram.")
    parser.add_argument('--df', type=str, default='data/gh_fn_code.csv',
                        help="Path to .csv file with function code")
    parser.add_argument('--tokenizer', type=str, default=None,
                        help="Path to .json tokenizer file for tokenizer instance")
    parser.add_argument('--train_text', type=str, default='data/fasttext_train.txt',
                        help=("Path to text file containing tokens for model. "
                              "Each line is whitespace separated tokens for a function."))
    parser.add_argument('--restart', action='store_true', default=False,
                        help="Whether to recreate train text file.")
    return parser.parse_args()


def create_train_tokens(df, tokenizer_file=None):
    if tokenizer_file is None:
        print("Training tokenizer...")
        all_code = (code_text for idx, code_text in df['code'].iteritems())
        tokenizer = train_tokenizer(all_code, 'data/gh-rust-tokenizer.json')
    else:
        print(f"Using pre-trained tokenizer from {tokenizer_file}")
        tokenizer = Tokenizer.from_file(tokenizer_file)

    def tokenize(code_text):
        return tokenizer.encode(code_text).tokens

    code_tokens = df['code'].apply(tokenize)

    return code_tokens


if __name__ == "__main__":
    args = passed_arguments()

    if args.restart:
        df = pd.read_csv(args.df)
        code_tokens = create_train_tokens(df, args.tokenizer)

        with open(args.train_text, 'w', encoding='utf8') as f:
            for idx, row in code_tokens.iteritems():
                f.write(' '.join(row) + '\n')

    model = fasttext.train_unsupervised(args.train_text)
    model.save_model('data/gh_skipgram.bin')

