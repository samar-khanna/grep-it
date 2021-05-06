import os
import argparse
import fasttext
import numpy as np
import pandas as pd
from tokenizers import Tokenizer
from data.rust_tokenizer import train_tokenizer
from sklearn.feature_extraction.text import TfidfVectorizer


def passed_arguments():
    parser = argparse.ArgumentParser(description="Script to train fasttext skipgram.")
    parser.add_argument('--df', type=str, default='data/gh_fn_code.csv',
                        help="Path to .csv file with function code")
    parser.add_argument('--tokenizer', type=str, default=None,
                        help="Path to .json tokenizer file for tokenizer instance")
    parser.add_argument('--train_text', type=str, default='data/gh_fasttext_train.txt',
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


def get_code_embedding(fn_tokens, fn_id, model, tfidf, tok_to_id):
    # Each word vector is d dimensional, let's say we have n tokens
    vecs = np.array([model.get_word_vector(tok) for tok in fn_tokens])  # (n, d)
    tok_ids = [tok_to_id[tok] for tok in fn_tokens]  # (n,)
    fn_tfidf = tfidf[fn_id, tok_ids].reshape(-1, 1)  # (n, 1)

    if len(fn_tfidf) > 0:
        embedding = np.mean(fn_tfidf * vecs, axis=0)
        return embedding / np.linalg.norm(embedding)
    else:
        return model.get_sentence_vector(' '.join(fn_tokens))


if __name__ == "__main__":
    args = passed_arguments()

    # if args.restart:
    df = pd.read_csv(args.df)
    code_tokens = create_train_tokens(df, args.tokenizer)
    space_sep_tokens = code_tokens.apply(lambda toks: ' '.join(toks))

    with open(args.train_text, 'w', encoding='utf8') as f:
        for idx, row in space_sep_tokens.iteritems():
            f.write(row + '\n')

    model = fasttext.train_unsupervised(args.train_text, bucket=20000, dim=200)
    model.save_model('data/gh_rust_code/gh_skipgram.bin')

    print("Getting TF-IDF matrix...")
    model = fasttext.load_model('data/gh_rust_code/gh_skipgram.bin')
    vectorizer = TfidfVectorizer(analyzer=str.split)
    code_tfidf = vectorizer.fit_transform(space_sep_tokens).toarray()
    tok_to_id = {tok: i for i, tok in enumerate(vectorizer.get_feature_names())}

    # print("Averaging word vectors based on TF-IDF scores...")
    code_embedding = [get_code_embedding(fn_tokens, fn_id, model, code_tfidf, tok_to_id)
                      for fn_id, fn_tokens in enumerate(code_tokens)]
    # code_embedding = [model.get_sentence_vector(' '.join(tokens))
    #                   for tokens in code_tokens]
    np.save('data/gh_rust_code/embedding.npy', np.array(code_embedding, dtype=np.float32))



