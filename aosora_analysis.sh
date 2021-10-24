#!/bin/bash

files_org="./aosora/*"
dir_utf8="./aosora_utf8/"
suffix_utf8='_utf8.txt'

# convert to UTF-8
for filepath in $files_org; do
  filename_utf8=$(basename $filepath '.txt')$suffix_utf8
  nkf -w $filepath > $dir_utf8$filename_utf8
done

# preprocess sentences
python preprocess.py --in-dir $dir_utf8 --out-file aosora_sentences.txt

# parse with Juman
cat aosora_sentences.txt | jumanpp > aosora_juman_sentences.txt

# extract phoneme balance sentences
python extract_balance_sentence.py --in-org-file aosora_sentences.txt --in-juman-file aosora_juman_sentences.txt --out-file extracted_sentences.txt
