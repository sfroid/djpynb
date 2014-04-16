import json

from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.http import require_GET

from reddit.models import RedditPost
from reddit.scraper import subreddits

PAGE_SIZE = 10

def getPosts(subr, page, page_size=None):
    if page_size is None:
        page_size = PAGE_SIZE
    if subr == '':
        posts = RedditPost.objects.order_by('added_date').reverse()[page_size*(page-1):page_size*page]
    else:
        posts = RedditPost.objects.filter(subreddit=subr).order_by('added_date').reverse()[page_size*(page-1):page_size*page]
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

def jsonifyPosts(posts):
    data = []
    for post in posts:
        pdata = {
            'subreddit': post.subreddit,
            'linkToPage': post.linkToPage,
            'title': post.title,
            'ncomments': post.ncomments,
            'url': post.url,
        }
        data.append(pdata)
    return json.dumps(data)

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
        "##".join(['path = ' + path, ', page = ' + request.GET.get('page', "no page")])))


def api_get_posts(request):
    subr = request.GET.get('subr', 'funny')
    page = int(request.GET.get('page', 1))
    count = int(request.GET.get('count', 10))

    print "got arguments %s, %s, %s"%(subr, page, count)

    if subr not in subreddits:
        return HttpResponse("Got a bad subreddit - %s."%subr)

    posts = getPosts(subr, page, count)

    return HttpResponse(jsonifyPosts(posts))


@require_GET
def api_v1(request, **kw):
    path = kw.get('path', None)
    if path is None:
        return HttpResponse("Got a bad path - %s."%str(path))

    if path == 'get_posts':
        return api_get_posts(request)

    return HttpResponse("Api not supported - %s."%path)

    #return HttpResponse("Hello, world. You're at the reddit api.\n Got args %s"%str(kw))
