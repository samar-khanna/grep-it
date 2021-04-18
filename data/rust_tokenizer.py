import re
import pandas as pd
from tokenizers import Tokenizer, Regex
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.normalizers import Replace
import tokenizers.pre_tokenizers as pre_tokenizers
from tokenizers.pre_tokenizers import Punctuation, Whitespace


def get_code_from_text(text):
    code_pattern = re.compile(r'(?<=\<code\>)(.+?)(?=\</code\>)', re.DOTALL)
    matches = re.findall(code_pattern, text)
    return '\n'.join(matches)


def train_tokenizer(all_text, out_file='data/rust-tokenizer.json'):
    tokenizer = Tokenizer(BPE(unk_token="[UNK]"))
    trainer = BpeTrainer(special_tokens=["[UNK]", "[CLS]", "[SEP]", "[PAD]", "[MASK]"])

    bracket_regexp = Regex(r'[{}();]')
    bracket_normalizer = Replace(bracket_regexp, ' ')

    camel_case_regexp = Regex(r'(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])')
    camel_case = pre_tokenizers.Split(camel_case_regexp, behavior='isolated')

    pre_tokenizer = pre_tokenizers.Sequence([camel_case, Punctuation(), Whitespace()])

    tokenizer.normalizer = bracket_normalizer
    tokenizer.pre_tokenizer = pre_tokenizer

    tokenizer.train_from_iterator(all_text, trainer=trainer)

    tokenizer.save(out_file)

    return tokenizer


def add_code_tokens(data_frame, tokenizer_file=None):
    print("Getting code from body text...")
    q_code = data_frame['q_body'].apply(get_code_from_text)
    a_code = data_frame['a_body'].apply(get_code_from_text)

    if tokenizer_file is None:
        print("Training tokenizer...")
        concat_code = pd.concat([q_code, a_code])
        all_code = (code_text for idx, code_text in concat_code.iteritems())
        tokenizer = train_tokenizer(all_code)
    else:
        print(f"Using pre-trained tokenizer from {tokenizer_file}")
        tokenizer = Tokenizer.from_file(tokenizer_file)

    print("Encoding the code as tokens...")

    def tokenize(text):
        return [s.lower() for s in tokenizer.encode(text).tokens]

    q_code_tokens = q_code.apply(tokenize)
    a_code_tokens = a_code.apply(tokenize)

    data_frame['q_code_tokens'] = q_code_tokens
    data_frame['a_code_tokens'] = a_code_tokens

    print("Done adding q_code_tokens and a_code_tokens!")

    return data_frame


if __name__ == "__main__":
    df = pd.read_csv('data/so_rust.csv')
    new_df = add_code_tokens(df, 'data/rust-tokenizer.json')
    new_df.to_csv('data/so_rust_code.csv')
