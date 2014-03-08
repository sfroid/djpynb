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

import praw, time
from reddit.models import RedditPost
import logging

polltime = 60*60.0 # 60 mins
userAgent = "jugad_scraper"
POSTS_TO_LOAD = 20
MAX_TITLE_LEN = 290
MAX_URL_LEN = 290
MAX_LINK_LEN = 290
MAX_SUBR_LEN = 90

subreddits = ['funny',
              'wtf',
              'earthporn',
              'aww',
              'standupshots',
              ]

sleepTime = polltime/len(subreddits)

def isPostInDB(post):
    return RedditPost.isAlreadyInDB(post)

def addPostToDB(subr, post):
    title = post.title[:MAX_TITLE_LEN]
    ncomments = post.num_comments
    url = post.url[:MAX_URL_LEN]
    if "imgur.com" in url:
        if len(url.split('/')[-1].split('.')) == 1:
            url += ".jpg"

    linkToPage = post.short_link[:MAX_LINK_LEN]
    subs = subr[:MAX_SUBR_LEN]
    logging.debug("adding the post:\n%s\n\n"%("\n".join([subr, title,
                url, linkToPage, str(ncomments)])))
    newPost = RedditPost(
            title=title,
            url=url,
            linkToPage=linkToPage,
            ncomments=ncomments,
            subreddit=subr,
        )
    newPost.save()

def startScraping():
    while 1:
        try:
            redreader = praw.Reddit(user_agent=userAgent)
            for subr in subreddits:
                try:
                    for post in redreader.get_subreddit(subr).get_hot(limit=POSTS_TO_LOAD):
                        if isPostInDB(post):
                            logging.debug("%s already in db"%post.title)
                            continue
                        addPostToDB(subr, post)
                except:
                    logging.exception("Error in getting and saving posts")
                logging.info("sleeping for %s secs after %s"%(sleepTime, subr))
                time.sleep(sleepTime)
        except:
            logging.exception("Error in using api scraper")



if __name__ == "__main__":
    startScraping()
