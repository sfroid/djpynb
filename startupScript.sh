#!/bin/bash

cd /home/sfroid/website/pynb/programs
bash ./restartipynb.sh

cd /home/sfroid/website/django
source bin/activate
cd sfroid/reddit

pkill -9 -f scraper.py
python scraper.py &
disown
