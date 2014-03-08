# source the environment
source ../bin/activate

# restart the reddit scraper
pkill -9 -f scraper.py
python reddit/scraper.py &
disown

# restart django/gunicorn
sudo supervisorctl restart sfroidsvr
