StockParser
===========

usage:
$ ./parser.py [-h] [-c COMPANY] [-y YEAR] [-m MONTH] -f FILEPATH
-c <company name>
-m <month>
-y <year>
-f </path/to/csv_file>

Example:
--------
$ ./parser.py -c "Company A" -f ../csv/data.csv

$ ./parser.py -c "Company A" -m Jan -f ../csv/data.csv

$ ./parser.py -c "Company A" -m Jan -y 1990 -f ../csv/data.csv


Make scripts executables
------------------------
1. Make parser.py executable
$ sudo chmod +x parser.py

2. Make test_parser.py executable
$ sudo chmod +x test_parser.py
