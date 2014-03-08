from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.http import require_GET

from reddit.models import RedditPost

PAGE_SIZE = 10

def getPosts(subr, page):
    if subr == '':
        posts = RedditPost.objects.order_by('added_date').reverse()[PAGE_SIZE*(page-1):PAGE_SIZE*page]
    else:
        posts = RedditPost.objects.filter(subreddit=subr).order_by('added_date').reverse()[PAGE_SIZE*(page-1):PAGE_SIZE*page]
    return posts

def getSubreddit(path):
    from .scraper import subreddits
    if path.startswith('debug'):
        subr = 'debug'
    else:
        subr = path.split('/')[0]
        if not subr in subreddits:
            subr = ''

    return subr

@require_GET
def home(request, **kw):

    path = kw.get('path', '')
    subr = getSubreddit(path)

    try:
        page = int(request.GET.get('page', 1))
    except:
        page = 1

    prevlink = "?page=%s"%(str(page-1)) if page > 1 else "?page=1"
    nextlink = "?page=%s"%(str(page+1))

    if not subr == 'debug':
        posts = getPosts(subr, page)
        return render_to_response('homeview.html',
                                  {'posts':posts,
                                   'prevlink': prevlink,
                                   'nextlink': nextlink,})

    return HttpResponse("Got args %s"%(
        "##".join(['path =' + path, 'page=' + request.GET.get('page', "no page")])))

@require_GET
def api(request, **kw):
    return HttpResponse("Hello, world. You're at the reddit api.\n Got args %s"%str(kw))
