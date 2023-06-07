#!/usr/bin/env sh
mkdir -p ./reports/
awk -F ',' '{print $3}' ./data/daily-stats.csv | tail -n+2 | asciigraph -h 10 -w 100 -c "Percent Levels (in %)" -sc "yellow" > ./reports/latest-usage.txt
cat ./reports/latest-usage.txt
