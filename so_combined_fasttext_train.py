import re
import argparse
import fasttext
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from tokenizers import Tokenizer
from data.rust_tokenizer import train_tokenizer as train_code_tokenizer
from data.language_tfidf import train_tokenizer as train_language_tokenizer


def passed_arguments():
    parser = argparse.ArgumentParser(description="Script to train fasttext skipgram.")
    parser.add_argument('--df', type=str, default='data/so_rust.csv',
                        help="Path to .csv file with function code")
    parser.add_argument('--lang_tokenizer', type=str, default=None,
                        help="Path to .json tokenizer file for language tokenizer instance")
    parser.add_argument('--code_tokenizer', type=str, default=None,
                        help="Path to .json tokenizer file for code tokenizer instance")
    parser.add_argument('--train_text', type=str, default='data/so_fasttext_train.txt',
                        help="Path to .txt file containing tokens for model.")
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


def create_train_tokens(df, lang_tokenizer_file=None, code_tokenizer_file=None):
    q_text = df['q_body'].apply(get_language_from_text)
    a_text = df['a_body'].apply(get_language_from_text)
    q_title = df['q_title']

    if lang_tokenizer_file is None:
        print("Training tokenizer...")
        concat_text = pd.concat([q_title, q_text, a_text])
        all_text = (text for idx, text in concat_text.iteritems())
        lang_tokenizer = train_language_tokenizer(
            all_text, 'data/so_rust_qa_combined/lang_tokenizer.json'
        )
    else:
        print(f"Using pre-trained tokenizer from {lang_tokenizer_file}")
        lang_tokenizer = Tokenizer.from_file(lang_tokenizer_file)

    q_code = df['q_body'].apply(get_code_from_text)
    a_code = df['a_body'].apply(get_code_from_text)

    if code_tokenizer_file is None:
        print("Training tokenizer...")
        concat_code = pd.concat([q_code, a_code])
        all_code = (text for idx, text in concat_code.iteritems())
        code_tokenizer = train_code_tokenizer(
            all_code, 'data/so_rust_qa_combined/code_tokenizer.json'
        )
    else:
        print(f"Using pre-trained tokenizer from {code_tokenizer_file}")
        code_tokenizer = Tokenizer.from_file(code_tokenizer_file)

    def lang_tokenize(txt):
        return lang_tokenizer.encode(txt).tokens

    def code_tokenize(txt):
        return code_tokenizer.encode(txt).tokens

    q_lang_text = (q_title + ' ' + q_text).apply(lang_tokenize)
    q_code_text = q_code.apply(code_tokenize)
    a_lang_text = a_text.apply(lang_tokenize)
    a_code_text = a_code.apply(code_tokenize)

    return q_lang_text + q_code_text + a_lang_text + a_code_text


if __name__ == "__main__":
    args = passed_arguments()

    df = pd.read_csv(args.df)
    train_tokens = create_train_tokens(df, args.lang_tokenizer, args.code_tokenizer)
    space_sep_tokens = train_tokens.apply(lambda toks: ' '.join(toks))

    with open(args.train_text, 'w', encoding='utf8') as f:
        for row in space_sep_tokens:
            f.write(row + '\n')

    model = fasttext.train_unsupervised(args.train_text, bucket=20000, dim=400)
    model.save_model('data/so_rust_qa_combined/so_skipgram.bin')

    embedding = [model.get_sentence_vector(tok_line) for tok_line in space_sep_tokens]
    np.save('data/so_rust_qa_combined/embedding.npy', np.array(embedding, dtype=np.float32))
