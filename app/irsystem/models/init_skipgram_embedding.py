import fasttext
import numpy as np
import pandas as pd

from tokenizers import Tokenizer

gh_code_metadata = pd.read_csv('./data/gh_code_metadata.csv')
gh_rust_tokenizer = Tokenizer.from_file('./data/gh-rust-tokenizer.json')
gh_rust_code_model = fasttext.load_model('./data/gh_skipgram.bin')
gh_code_vecs = np.load('./data/gh_code_embedding.npy')





