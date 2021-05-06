import fasttext
import numpy as np
import pandas as pd

from tokenizers import Tokenizer

gh_code_metadata = pd.read_csv('./data/gh_fn_metadata.csv')
gh_rust_tokenizer = Tokenizer.from_file('./data/gh_rust_code/tokenizer_vocab.json')
gh_rust_code_model = fasttext.load_model('./data/gh_rust_code/gh_skipgram.bin')
gh_code_vecs = np.load('./data/gh_rust_code/embedding.npy')

so_metadata = pd.read_csv('./data/so_rust.csv')

so_code_tokenizer = Tokenizer.from_file('./data/so_rust_qa_code/tokenizer_vocab.json')
# so_code_model = fasttext.load_model('./data/so_rust_qa_code/so_code_skipgram.bin')
# so_code_vecs = np.load('./data/so_rust_qa_code/embedding.npy')

so_lang_tokenizer = Tokenizer.from_file('./data/so_rust_qa_lang/tokenizer_vocab.json')
# so_lang_model = fasttext.load_model('./data/so_rust_qa_lang/so_language_skipgram.bin')
# so_lang_vecs = np.load('./data/so_rust_qa_lang/embedding.npy')

so_model = fasttext.load_model('./data/so_rust_qa_combined/so_skipgram.bin')
so_vecs = np.load('./data/so_rust_qa_combined/embedding.npy')




