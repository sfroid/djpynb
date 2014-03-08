from django.db import models

class RedditPost(models.Model):
    title = models.CharField(max_length=300)
    url = models.CharField(max_length=300)
    linkToPage = models.CharField(max_length=300)
    ncomments = models.IntegerField()
    added_date = models.DateTimeField(db_index=True, auto_now_add=True)
    subreddit = models.CharField(db_index=True, max_length=100)

    @staticmethod
    def isAlreadyInDB(post):
        if len(RedditPost.objects.filter(linkToPage=post.short_link)):
            return True
        return False

    def __unicode__(self):
        rv = self.title
        return (rv[:50] + "...") if len(rv) > 50 else rv
