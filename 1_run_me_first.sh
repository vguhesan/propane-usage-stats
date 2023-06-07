#!/usr/bin/env bash

echo -e "\n################################################################"
echo -e "# This script should be called the first time you are running"
echo -e "# this project. It sets up the Python Virtual Environment and"
echo -e "# installs all the necessary dependent packages.\n#"
echo -e "# You do not need to run this script each time."
echo -e "################################################################\n"

pipenv install

mkdir -p data

if [ ! -f ./data/daily-stats.csv ]
then
    echo -e "\nCreating file /data/daily-stats.csv...\n"
    echo "timestamp,gallonsRemaining,percentRemaining" > ./data/daily-stats.csv
else
    echo -e "\nSkipping creation of ./data/daily-stats.csv (since it already exists)\n"
fi

echo -e "You can now invoke the script in this way:\n"
echo -e "pipenv run ./collect_tank_statistics.py \"USERID\" \"PASSWORD\" >> ./data/daily-stats.csv"
echo -e "\n"