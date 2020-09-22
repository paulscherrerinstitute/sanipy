#!/bin/bash

./sani.py check data/test_chans_good.txt -s
echo
./sani.py check data/test_chans_bad.txt
echo
./sani.py compare data/test1.csv data/test4
echo
./sani.py compare data/test1.csv data/test4 -v


