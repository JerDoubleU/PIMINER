#!/usr/bin/env bash

PATTERNS='patterns.txt'
DIR='CLEANED_DATA'

# show all patterns matching those in the patterns.txt file
grep -f ${PATTERNS} -C 1 ${DIR}/*
