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

testing = False

def processPosts():
    for post in RedditPost.objects.all():
        subr = post.subreddit

        if not subr.islower():
            newSubr = subr.lower()
            print "%s    ----    %s"%(subr, newSubr)
            if not testing:
                post.subreddit = newSubr
                post.save()

import time
st = time.time()
processPosts()
print "took %8.6f secs"%(time.time() - st)

