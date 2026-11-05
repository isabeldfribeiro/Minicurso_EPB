#!/bin/bash

mkdir -p ../out_rgi

for arquivo in ../replicons/*.fasta; do

    nome=$(basename "$arquivo" .fasta)

    mkdir -p "../out_rgi/$nome"

    rgi main \
        -i "$arquivo" \
        -o "../out_rgi/$nome/$nome" \
        -t contig \
        -a DIAMOND \
        -n 10

done
