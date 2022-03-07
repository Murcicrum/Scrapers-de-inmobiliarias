#!/bin/bash

LOG_FILE=where/is/log_file.txt
DATE=$(date +%Y-%m-$d-%H:%M)

echo "$DATE start scraper1" >> $LOG_FILE
path/to/scraper1.py $1 2>>$LOG_FILE

echo "$DATE start scraper2" >> $LOG_FILE
path/to/scraper2.py $1 2>>$LOG_FILE

echo "$DATE start scraper3" >> $LOG_FILE
path/to/scraper3.py $1 2>>$LOG_FILE

