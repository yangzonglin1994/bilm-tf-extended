import argparse
import os
import sys

import numpy.random as rdm

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(PROJECT_ROOT)

from utils import tools
from utils import reader
from utils.tools import my_getattr

rdm.seed(1234)


def main(args):
    current_func_name = sys._getframe().f_code.co_name
    if args.train_data in [args.split_train_dir, args.split_heldout_dir]:
        print('\n======== In', current_func_name, '========')
        print('Raw data and split data path are the same.')
        print('No split.')
        return

    total_train_line_cnt = reader.count_lines(args.train_data, args.encoding)
    train_data = args.train_data
    if os.path.isfile(train_data):
        train_data = [train_data]
    elif os.path.isdir(train_data):
        train_data = tools.get_fnames_under_path(train_data)

    if not os.path.exists(args.split_train_dir):
        os.makedirs(args.split_train_dir)
    if not os.path.exists(args.split_heldout_dir):
        os.makedirs(args.split_heldout_dir)
    if args.test_samples_num != total_train_line_cnt:
        tools.del_file_under_path(args.split_train_dir)
    if args.test_samples_num != 0:
        tools.del_file_under_path(args.split_heldout_dir)

    split_train_files = []
    for i in range(args.split_train_num):
        train_split_file = open(os.path.join(args.split_train_dir, 'train-'+str(i)), 'w', encoding=args.encoding)
        split_train_files.append(train_split_file)
    split_heldout_files = []
    for i in range(args.split_heldout_num):
        heldout_split_file = open(os.path.join(args.split_heldout_dir, 'heldout-'+str(i)), 'w', encoding=args.encoding)
        split_heldout_files.append(heldout_split_file)

    def random_togo(num):
        suffix = round(rdm.rand() * num)
        suffix = 0 if suffix < 0 else suffix
        suffix = num - 1 if suffix >= num else suffix
        return suffix

    test_ratio = args.test_samples_num / total_train_line_cnt
    line_cnt = 0
    for fname in train_data:
        with open(fname, 'r', encoding=args.encoding) as file:
            for line in file:
                if rdm.rand() < test_ratio:
                    split_heldout_files[random_togo(args.split_heldout_num)].write(line)
                else:
                    split_train_files[random_togo(args.split_train_num)].write(line)
                line_cnt += 1
                if line_cnt % 10000 == 0:
                    print(line_cnt, 'lines have been processed.')
    print('=================================================')
    print(line_cnt, 'lines have been processed finally.')

    for file in split_train_files + split_heldout_files:
        file.close()

    print('split train data total samples count:', reader.count_lines(args.split_train_dir, args.encoding))
    print('split heldout data total samples count:', reader.count_lines(args.split_heldout_dir, args.encoding))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--train-data', type=str, metavar='STR', required=True, help='train data')
    parser.add_argument('--split-train-dir', type=str, metavar='STR', required=True,
                        help='dir to store split train data')
    parser.add_argument('--split-heldout-dir', type=str, metavar='STR', required=True,
                        help='dir to store split test data')
    parser.add_argument('--split-train-num', type=int, metavar='N', required=True,
                        help='the number of split train data files')
    parser.add_argument('--split-heldout-num', type=int, metavar='N', required=True,
                        help='the number of split held-out data files')
    parser.add_argument('--test-samples-num', type=int, metavar='N', required=True,
                        help='the number of test data samples')
    parser.add_argument('--encoding', type=str, metavar='STR', help='open and save encoding')
    parser.add_argument('--debug', action='store_true', help='whether to show more info for debug')

    args = parser.parse_args()
    args.encoding = my_getattr(args, 'encoding', 'utf-8')
    args.debug = getattr(args, 'debug', False)

    main(args)
