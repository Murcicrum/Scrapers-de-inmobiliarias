#!/bin/bash
#

LOG_FILE=where/is/log_file.txt

echo "$(date +%Y-%m-$d-%H:%M) start scraper1" >> $LOG_FILE
path/to/scraper1.py $1 2>>$LOG_FILE

echo "$(date +%Y-%m-$d-%H:%M) start scraper2" >> $LOG_FILE
path/to/scraper2.py $1 2>>$LOG_FILE

echo "$(date +%Y-%m-$d-%H:%M) start scraper3" >> $LOG_FILE
path/to/scraper3.py $1 2>>$LOG_FILE

