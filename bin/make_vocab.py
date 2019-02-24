import argparse
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(PROJECT_ROOT)

from utils import tools
from utils.tools import my_getattr


def main(args):
    vocab = {}
    train_data = args.train_data
    if os.path.isfile(train_data):
        train_data = [train_data]
    elif os.path.isdir(train_data):
        train_data = tools.get_fnames_under_path(train_data)

    for fname in train_data:
        with open(fname, 'r', encoding=args.encoding) as file:
            for line in file:
                for token in line.split():
                    if vocab.get(token) is not None:
                        vocab[token] += 1
                    else:
                        vocab[token] = 1
    sorted_vocab = sorted(vocab, key=vocab.get, reverse=True)
    vocab_url_dir = os.path.dirname(args.vocab_fname)
    if not os.path.exists(vocab_url_dir):
        os.makedirs(vocab_url_dir)
    with open(args.vocab_fname, 'w', encoding=args.encoding) as out_file:
        out_file.write(args.bos + '\n')
        out_file.write(args.eos + '\n')
        out_file.write(args.unk + '\n')
        for token in sorted_vocab:
            out_file.write(token)
            if args.debug:
                out_file.write(' => ' + str(vocab.get(token)))
            out_file.write('\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--train-data', type=str, metavar='STR', required=True, help='train data')
    parser.add_argument('--vocab-fname', type=str, metavar='STR', required=True, help='vocabulary file')
    parser.add_argument('--encoding', type=str, metavar='STR', help='open and save encoding')
    parser.add_argument('--debug', action='store_true', help='whether to show more info for debug')
    parser.add_argument('--bos', type=str, metavar='STR', help='special symbol for begin of sen')
    parser.add_argument('--eos', type=str, metavar='STR', help='special symbol for end of sen')
    parser.add_argument('--unk', type=str, metavar='STR', help='special symbol for unknown token')

    args = parser.parse_args()
    args.encoding = my_getattr(args, 'encoding', 'utf-8')
    args.debug = getattr(args, 'debug', False)
    args.bos = my_getattr(args, 'bos', '<S>')
    args.eos = my_getattr(args, 'eos', '</S>')
    args.unk = my_getattr(args, 'unk', '<UNK>')

    main(args)
