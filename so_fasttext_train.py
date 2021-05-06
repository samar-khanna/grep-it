import re
import argparse
import fasttext
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from tokenizers import Tokenizer
from data.rust_tokenizer import train_tokenizer as code_tokenizer
from data.language_tfidf import train_tokenizer as language_tokenizer


def passed_arguments():
    parser = argparse.ArgumentParser(description="Script to train fasttext skipgram.")
    parser.add_argument('--df', type=str, default='data/so_rust.csv',
                        help="Path to .csv file with function code")
    parser.add_argument('--lang_tokenizer', type=str, default=None,
                        help="Path to .json tokenizer file for language tokenizer instance")
    parser.add_argument('--code_tokenizer', type=str, default=None,
                        help="Path to .json tokenizer file for code tokenizer instance")
    parser.add_argument('--lang_text', type=str, default='data/so_fasttext_lang_train.txt',
                        help=("Path to text file containing tokens for model. "
                              "Line is whitespace separated tokens for q_title, q_body, a_body"))
    parser.add_argument('--code_text', type=str, default='data/so_fasttext_code_train.txt',
                        help=("Path to text file containing tokens for model. "
                              "Line is whitespace separated tokens for q_code, a_code"))
    return parser.parse_args()


def get_language_from_text(text):
    soup = BeautifulSoup(text, features="html.parser")
    for s in soup.select('code'):
        s.decompose()
    return soup.get_text()


def get_code_from_text(text):
    code_pattern = re.compile(r'(?<=\<code\>)(.+?)(?=\</code\>)', re.DOTALL)
    matches = re.findall(code_pattern, text)
    return '\n'.join(matches)


def create_language_tokens(df, lang_tokenizer_file=None):
    q_text = df['q_body'].apply(get_language_from_text)
    a_text = df['a_body'].apply(get_language_from_text)
    q_title = df['q_title']

    if lang_tokenizer_file is None:
        print("Training tokenizer...")
        concat_text = pd.concat([q_title, q_text, a_text])
        all_text = (text for idx, text in concat_text.iteritems())
        tokenizer = language_tokenizer(all_text, 'data/so-language-tokenizer.json')
    else:
        print(f"Using pre-trained tokenizer from {lang_tokenizer_file}")
        tokenizer = Tokenizer.from_file(lang_tokenizer_file)

    qa_text = q_title + ' ' + q_text + ' ' + a_text
    qa_tokens = qa_text.apply(lambda text: tokenizer.encode(text).tokens)

    return qa_tokens


def create_code_tokens(df, code_tokenizer_file=None):
    q_code = df['q_body'].apply(get_code_from_text)
    a_code = df['a_body'].apply(get_code_from_text)

    if code_tokenizer_file is None:
        print("Training tokenizer...")
        concat_text = pd.concat([q_code, a_code])
        all_text = (text for idx, text in concat_text.iteritems())
        tokenizer = code_tokenizer(all_text, 'data/so-rust-tokenizer.json')
    else:
        print(f"Using pre-trained tokenizer from {code_tokenizer_file}")
        tokenizer = Tokenizer.from_file(code_tokenizer_file)

    qa_code = q_code + ' ' + a_code
    qa_tokens = qa_code.apply(lambda text: tokenizer.encode(text).tokens)

    return qa_tokens


if __name__ == "__main__":
    args = passed_arguments()

    df = pd.read_csv(args.df)
    lang_tokens = create_language_tokens(df, args.lang_tokenizer)
    code_tokens = create_code_tokens(df, args.code_tokenizer)

    with open(args.lang_text, 'w', encoding='utf8') as f:
        for idx, row in lang_tokens.iteritems():
            f.write(' '.join(row) + '\n')

    with open(args.code_text, 'w', encoding='utf8') as f:
        for idx, row in code_tokens.iteritems():
            f.write(' '.join(row) + '\n')

    model_language = fasttext.train_unsupervised(args.lang_text, bucket=20000)
    model_language.save_model('data/so_rust_lang/so_language_skipgram.bin')
    language_embedding = [model_language.get_sentence_vector(' '.join(tokens))
                          for tokens in lang_tokens]
    np.save('data/so_rust_lang/so_lang_embedding.npy',
            np.array(language_embedding, dtype=np.float32))

    model_code = fasttext.train_unsupervised(args.code_text, bucket=20000)
    model_code.save_model('data/so_rust_code/so_code_skipgram.bin')
    code_embedding = [model_code.get_sentence_vector(' '.join(tokens))
                      for tokens in code_tokens]
    np.save('data/so_rust_code/so_code_embedding.npy',
            np.array(code_embedding, dtype=np.float32))






