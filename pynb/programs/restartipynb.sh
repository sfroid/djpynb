source ../bin/activate

pkill -9 -f nbwatcher
pkill -9 -f "profile=nbserver"
pkill -9 -f gotyourbackup

python nbwatcher.py &
disown

python gotyourbackup.py &
disown

cd ../notebooks
ipython notebook --profile=nbserver &
disown
