import os
import re
import csv
import logging
import subprocess
import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", default="./data/gh_rust_5+.csv", type=str, help="Path to the csv file")
parser.add_argument("--output", "-out", default="./data/gh_fn_code.csv", type=str, help="Path to the csv file")
parser.add_argument("--lsp-path", "-l", default="./bin/rust-analyzer", type=str, help="Path to the rust-analyzer file")
args = parser.parse_args()

RUST_ANALYZER_PATH = args.lsp_path

def get_parse_tree(code):
    parse_tree = subprocess.run([RUST_ANALYZER_PATH, "parse"], stdout=subprocess.PIPE, text=True, input=code)
    return parse_tree.stdout

def get_symbol_table(code):
    symbols = subprocess.run([RUST_ANALYZER_PATH, "symbols"], stdout=subprocess.PIPE, text=True, input=code)
    return symbols.stdout

def tokenize_parse_tree(parse_tree, ignore_whitespace=True, merge_comments=True):
    tokens = []
    for line in parse_tree.split("\n"):
        if len(line) == 0:
            continue
        line = line.strip()
        token, additional_str = tuple(line.split("@", 1))
        if token == "WHITESPACE":
            continue
        splitted = additional_str.split(" ", 1)
        start, end = tuple(map(int, splitted[0].split("..")))

        if merge_comments and len(tokens) > 0 and tokens[-1][0] == "COMMENT" and token == "COMMENT":
            tokens[-1][1][1] = end
        else:
            tokens.append((token, [start, end]))
    return tokens

class Symbol:
    def __init__(self, label, node_range, navigate_range, kind):
        self.label = label
        self.node_range = node_range
        self.navigate_range = navigate_range
        self.kind = kind
        self.code = None
        self.docstring = None
        self.tokenized_parse_tree = []
        self.filename = None
        self.repo_name = None

    def handle_parse_tree(self, parse_tree: str, content: str):
        self.tokenized_parse_tree = tokenize_parse_tree(parse_tree)
        for token in self.tokenized_parse_tree:
            if token[0] == "COMMENT" and token[1][0] == 0:
                self.docstring = content[token[1][0]: token[1][1]]
                self.code = content[token[1][1]:]
                return
        self.code = content

    def is_function(self):
        return self.kind == "Function"
    
    def __repr__(self):
        return f"Symbol ( label: {self.label}, kind: {self.kind}, node_range: {self.node_range})"

    def to_dict(self):
        return {
            "repo_name": self.repo_name,
            "filename": self.filename,
            "label": self.label,
            "node_range": self.node_range,
            "navigate_range": self.navigate_range,
            "kind": self.kind,
            "code": self.code,
            "docstring": self.docstring,
            "tokenized_parse_tree": self.tokenized_parse_tree,
        }

    @staticmethod
    def parse(table: str):
        symbol_list = []
        for s in table.split("\n"):
            if len(s) == 0:
                continue

            p = re.compile("StructureNode \{ (.*) \}")
            result = p.search(s)
            structured_node = result.group(1)
            
            # Splitting on commas not iside parenthesis
            items = re.split(r',\s*(?![^()]*\))', structured_node)
            for item in items:
                k, v = tuple(item.split(":", 1))
                v = v.strip()
                if k == "label":
                    label = v.replace("\"", "")
                elif k == "navigation_range":
                    navigation_range = tuple(map(int, v.split("..")))
                elif k == "node_range":
                    node_range = tuple(map(int, v.split("..")))
                elif k == "kind":
                    p = re.compile("SymbolKind\((.*)\)")
                    result = p.search(v)
                    kind = result.group(1).strip()

            symbol = Symbol(label, node_range, navigation_range, kind)
            symbol_list.append(symbol)
        return symbol_list

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    if not os.path.isfile(RUST_ANALYZER_PATH):
        logging.error('Could not find rust-analyzer. Follow steps in README to download.')
        exit(1)

    keys = [
        "repo_name",
        "filename",
        "label",
        "node_range",
        "navigate_range",
        "kind",
        "code",
        "docstring",
        "tokenized_parse_tree",
    ]
    with open(args.output, 'w+') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()

    df = pd.read_csv(args.input)
    logging.info("Finished reading the csv...")

    df = df[df["stars"] > 1000]
    num_rows = df.shape[0]
    logging.info(f"Total number of rows: {num_rows}")
    i = 0
    for idx, row in df.iterrows():
        i += 1
        if i % 100 == 0:
            logging.info(f"Finished {i} / {num_rows} rows")
        try:
            symbols_table = get_symbol_table(row["content"])
            symbols = Symbol.parse(symbols_table)
        
            function_symbols = filter(lambda s: s.is_function(), symbols)

            with open(args.output, 'a+') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)

                for sym in function_symbols:
                    sym.repo_name = row["repo_name"]
                    sym.filename = row["path"]
                    content = row["content"][sym.node_range[0]: sym.node_range[1]]
                    parse_tree = get_parse_tree(content)
                    sym.handle_parse_tree(parse_tree, content)
                    dict_writer.writerow(sym.to_dict())
        except:
            continue
        

        
    