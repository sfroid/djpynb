##########################################################
##########################################################

# settings for the django project
import sys, os
PROJ_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJ_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sfroid.settings")

##########################################################
##########################################################

# normal code

from reddit.models import RedditPost


testing = True

def processPosts():
    for post in RedditPost.objects.all():
        url = post.url
        if "imgur.com" in url:
            if len(url.split('/')[-1].split('.')) == 2:
                if len(url.split('/')) > 4:
                    url2 = url[:-(len(url.split('.')[-1]) + 1)]
                    print "%s    ----    %s"%(url, url2)
                    if not testing:
                        post.url = url2
                        post.save()

import time
st = time.time()
processPosts()
print "took %8.6f secs"%(time.time() - st)

