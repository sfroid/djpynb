# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RedditPost'
        db.create_table(u'reddit_redditpost', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('linkToPage', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('ncomments', self.gf('django.db.models.fields.IntegerField')()),
            ('added_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('subreddit', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
        ))
        db.send_create_signal(u'reddit', ['RedditPost'])


    def backwards(self, orm):
        # Deleting model 'RedditPost'
        db.delete_table(u'reddit_redditpost')


    models = {
        u'reddit.redditpost': {
            'Meta': {'object_name': 'RedditPost'},
            'added_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'linkToPage': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'ncomments': ('django.db.models.fields.IntegerField', [], {}),
            'subreddit': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        }
    }

    complete_apps = ['reddit']