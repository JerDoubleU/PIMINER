#!/usr/bin/env bash

## This script is used to clean the elements in the DATA_TEST dir

DATA_DIR='raw_data'
CLEANED_DATA_DIR='cleaned_data'

for FILE in ${DATA_DIR}/*.txt
  do
    BASE="${FILE##*/}"
    OUTPUT="${CLEANED_DATA_DIR}/${BASE%.*}_cleaned.txt"

    # force convert to utf-8 for nonconformant characters
    iconv -f utf-8 -t utf-8 -c ${FILE} > ${OUTPUT}

    ## Add other cleaning operations here:

  done
echo 'Done'
