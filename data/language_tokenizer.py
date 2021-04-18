import re
import pandas as pd
from bs4 import BeautifulSoup
from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.normalizers import BertNormalizer
from tokenizers.pre_tokenizers import ByteLevel


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

    if tokenizer_file is None:
        print("Training tokenizer...")
        concat_text = pd.concat([q_text, a_text])
        all_text = (text for idx, text in concat_text.iteritems())
        tokenizer = train_tokenizer(all_text)
    else:
        print(f"Using pre-trained tokenizer from {tokenizer_file}")
        tokenizer = Tokenizer.from_file(tokenizer_file)

    print("Encoding the language as tokens...")

    def tokenize(text):
        return tokenizer.encode(text).tokens

    q_code_tokens = q_text.apply(tokenize)
    a_code_tokens = a_text.apply(tokenize)

    data_frame['q_body_tokens'] = q_code_tokens
    data_frame['a_body_tokens'] = a_code_tokens

    print("Done adding q_body_tokens and a_body_tokens!")

    return data_frame


if __name__ == "__main__":
    df = pd.read_csv('data/so_rust_code.csv')
    new_df = add_language_tokens(df)
    new_df.to_csv('data/so_rust_lang_code.csv')
