# sanipy

sanipy is a command-line tool for epics connection testing.

It has two commands ([check](#check) and [compare](#compare)) and a few option switches (check `sani.py -h` and `sani.py COMMAND -h`).

The `data` folder contains some channel lists and output files for testing.

## check

`./sani.py check data/test_chans_good.txt`

<img src="docs/check_good.png" width="491"> \

`./sani.py check data/test_chans_bad.txt`

<img src="docs/check_bad.png" width="491">


## compare

`./sani.py compare data/test1.csv data/test4 -v`

<img src="docs/compare_good.png" width="568"> \

`./sani.py compare data/test1.csv data/test3`

<img src="docs/compare_bad.png" width="658">

(Note here that `.csv` is automatically appended if missing.)
