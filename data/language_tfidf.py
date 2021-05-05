import os
import re
import ast
import json
import numpy as np
import pandas as pd
import scipy.sparse
from bs4 import BeautifulSoup

from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.normalizers import BertNormalizer
from tokenizers.pre_tokenizers import ByteLevel

from sklearn.feature_extraction.text import TfidfVectorizer

# TODO: Note, for now, to run this file move it up to grep-it dir


def get_language_from_text(text):
    soup = BeautifulSoup(text, features="html.parser")
    for s in soup.select('code'):
        s.decompose()
    return soup.get_text()


def train_tokenizer(all_text, out_file='data/language-tokenizer.json'):
    tokenizer = Tokenizer(BPE(unk_token="[UNK]"))
    trainer = BpeTrainer(special_tokens=["[UNK]", "[CLS]", "[SEP]", "[PAD]", "[MASK]"])

    tokenizer.normalizer = BertNormalizer()
    tokenizer.pre_tokenizer = ByteLevel()

    tokenizer.train_from_iterator(all_text, trainer=trainer)

    tokenizer.save(out_file)

    return tokenizer


def add_language_tokens(data_frame, tokenizer_file=None):
    print("Getting language from body text...")
    q_text = data_frame['q_body'].apply(get_language_from_text)
    a_text = data_frame['a_body'].apply(get_language_from_text)
    q_title = data_frame['q_title']

    if tokenizer_file is None:
        print("Training tokenizer...")
        concat_text = pd.concat([q_title, q_text, a_text])
        all_text = (text for idx, text in concat_text.iteritems())
        tokenizer = train_tokenizer(all_text)
    else:
        print(f"Using pre-trained tokenizer from {tokenizer_file}")
        tokenizer = Tokenizer.from_file(tokenizer_file)

    print("Encoding the language as tokens...")

    def tokenize(text):
        return tokenizer.encode(text).tokens

    q_title_tokens = q_title.apply(tokenize)
    q_code_tokens = q_text.apply(tokenize)
    a_code_tokens = a_text.apply(tokenize)

    data_frame['q_title_tokens'] = q_title_tokens
    data_frame['q_body_tokens'] = q_code_tokens
    data_frame['a_body_tokens'] = a_code_tokens

    print("Done adding q_body_tokens and a_body_tokens!")

    return data_frame


def create_tfidf(df):
    print("Preprocessing cosine data....")
    # qa_code_tokens = df['a_code_tokens']
    qa_tokens = pd.concat([
        df['q_title_tokens'], df['q_body_tokens'], df['a_body_tokens']
    ], axis=1)

    # TODO: Refactor this by saving tokens in correct format
    def tokenize(inp):
        return ' '.join(inp)
        # return ' '.join(ast.literal_eval(inp_str))

    qa_tokens = qa_tokens.applymap(tokenize)
    qa_tokens = qa_tokens['q_title_tokens'] + ' ' +\
                qa_tokens['q_body_tokens'] + ' ' + \
                qa_tokens['a_body_tokens']

    qa_vectorizer = TfidfVectorizer(analyzer=str.split)
    qa_tfidf = qa_vectorizer.fit_transform(qa_tokens)

    return qa_vectorizer, qa_tfidf


if __name__ == "__main__":
    df = pd.read_csv('data/so_rust.csv')
    new_df = add_language_tokens(df, 'data/language-tokenizer.json')
    # new_df = add_language_tokens(df)
    # new_df.to_csv('data/so_rust_lang_code.csv')

    os.makedirs('data/rust_qa_body', exist_ok=True)

    qa_body_vectorizer, qa_tfidf = create_tfidf(new_df)
    with open('data/rust_qa_body/vocab.json', 'w') as f:
        json.dump(qa_body_vectorizer.vocabulary_, f)

    np.save('data/rust_qa_body/idf.npy', qa_body_vectorizer.idf_)

    scipy.sparse.save_npz('data/rust_qa_body/tf_idf.npz', qa_tfidf)
