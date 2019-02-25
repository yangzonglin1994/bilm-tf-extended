#!/usr/bin/env bash

set -x
set -e

if [[ $# -ne 2 ]]; then
    echo 'Usage: operation dataset'
    exit -1
fi
operation=$1
dataset=$2

case "$operation" in
'make_vocab')
    python bin/make_vocab.py --train-data=data/${dataset}/${dataset}-train.bpe \
    --vocab-fname bin/processed/${dataset}.vocab
    ;;
'prepare_data')
    python bin/prepare_data.py --train-data=data/${dataset}/${dataset}-test.bpe \
    --split-train-dir=bin/processed/${dataset}-train/ \
    --split-heldout-dir=bin/processed/${dataset}-test/ \
    --split-train-num=0 --split-heldout-num=3 \
    --test-samples-num=3761
    ;;
'train_elmo')
    # like 2019-02-24_21:08:22
    CHECKPOINT_DIR=checkpoints/bilm-${dataset}_`date +%F_%T`
    mkdir -p ${CHECKPOINT_DIR}
    export CUDA_VISIBLE_DEVICES=0
    python bin/train_elmo.py \
        --train_prefix=bin/processed/${dataset}-train/* \
        --vocab_file=bin/processed/${dataset}.vocab \
        --save_dir=${CHECKPOINT_DIR}/
    ;;
'eval_elmo')
    export CUDA_VISIBLE_DEVICES=0
    python bin/run_test.py \
        --test_prefix=bin/processed/${dataset}-test/* \
        --vocab_file=bin/processed/${dataset}.vocab \
        --save_dir=checkpoints/bilm-ptb_2019-02-24_23:55:29
    ;;
*)
    echo 'error'
    ;;
esac
