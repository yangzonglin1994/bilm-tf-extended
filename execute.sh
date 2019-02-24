#!/usr/bin/env bash

if [[ $# -ne 1 ]]; then
    echo 'Usage: operation'
    exit -1
fi
operation=$1

case "$operation" in
'make_vocab')
    python bin/make_vocab.py --train-data=data/toy/toy-train.bpe \
    --vocab-fname bin/processed/toy.vocab
    ;;
'prepare_data')
    python bin/prepare_data.py --train-data=data/toy/toy-train.bpe \
    --split-train-dir=bin/processed/toy-train/ \
    --split-heldout-dir=bin/processed/toy-test/ \
    --split-train-num=0 --split-heldout-num=4 \
    --test-samples-num=40
    ;;
'train_elmo')
    python bin/train_elmo.py --train_prefix=bin/processed/toy-train/* \
    --vocab_file=bin/processed/toy.vocab \
    --save_dir=checkpoints/bilm-toy/
    ;;
*)
    echo 'error'
    ;;
esac
