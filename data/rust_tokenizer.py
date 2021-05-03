from tokenizers import Tokenizer, Regex
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.normalizers import Replace
import tokenizers.normalizers as normalizers
from tokenizers.normalizers import Lowercase
import tokenizers.pre_tokenizers as pre_tokenizers
from tokenizers.pre_tokenizers import Punctuation, Whitespace


def train_tokenizer(all_text, out_file='data/rust-tokenizer.json'):
    tokenizer = Tokenizer(BPE(unk_token="[UNK]"))
    trainer = BpeTrainer(special_tokens=["[UNK]", "[CLS]", "[SEP]", "[PAD]", "[MASK]"])

    syntax_regexp = Regex(r'[\[\]{}\(\);]|[=<>",_.&*\'\\]|::|->')
    camel_case_regexp = Regex(r'(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])')
    common_keyword_regexp = Regex(r'let|const|fn|if|else|self|println')
    small_var_regexp = Regex(r'\b(\w{1})\b\s?')  # or r'\b(\w{1,2})\b\s?'
    normalizer = normalizers.Sequence([
        Replace(syntax_regexp, ' '),  # removes unnecessary syntax
        Replace(camel_case_regexp, ' '),
        Lowercase(),
        Replace(common_keyword_regexp, ' '),
        Replace(small_var_regexp, ' ')
    ])

    # camel_case = pre_tokenizers.Split(camel_case_regexp, behavior='isolated')

    pre_tokenizer = pre_tokenizers.Sequence([Punctuation(), Whitespace()])

    tokenizer.normalizer = normalizer
    tokenizer.pre_tokenizer = pre_tokenizer

    # print(all_text)
    tokenizer.train_from_iterator(all_text, trainer=trainer)

    tokenizer.save(out_file)

    return tokenizer
