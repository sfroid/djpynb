source ../bin/activate

python nbwatcher.py &
disown

python gotyourbackup.py &
disown

cd ../notebooks
ipython notebook --profile=nbserver &
disown
