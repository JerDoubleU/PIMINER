#!/usr/bin/env bash

PATTERNS='patterns.txt'
DIR='cleaned_data'

# show all patterns matching those in the patterns.txt file
grep -f ${PATTERNS} -C 1 ${DIR}/*
