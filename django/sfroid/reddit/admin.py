from django.contrib import admin
from reddit.models import RedditPost

class RedditPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'subreddit', 'added_date')

admin.site.register(RedditPost, RedditPostAdmin)
