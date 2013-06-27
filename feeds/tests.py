"""
===========
feeds.tests
===========

Unit tests for feeds application.

"""

import datetime

from django.test import TestCase

from .models import Entry, Feed, Tag


TEST_FEED_TITLE = 'Shutdown Corner'
TEST_FEED_HREF = 'http://sports.yahoo.com/nfl/blog/shutdown_corner/rss.xml'

TEST_ENTRY_UID = (
    'urn:newsml:sports.yahoo,lego:19780928:top,article,'
    'da6e8220-8824-3dcf-a4fe-2a442b329392-l:1'
)
TEST_ENTRY_TITLE = 'Tim Tebow a tight end option for the Patriots? Not so fast'
TEST_ENTRY_LINK = (
    'http://sports.yahoo.com/blogs/nfl-shutdown-corner/'
    'tim-tebow-tight-end-option-patriots-not-fast-140838477.html'
)
TEST_ENTRY_PUBLISH_DATE = datetime.datetime.now() - datetime.timedelta(hours=1)
TEST_ENTRY_SUMMARY = 'Test entry summary'


class TestModels(TestCase):

    def test_feed_and_entry(self):
        feed = Feed.objects.create(title=TEST_FEED_TITLE,
                                   href=TEST_FEED_HREF)
        self.assertRaises(Feed.objects.create,
                          title=TEST_ENTRY_TITLE,
                          href=TEST_FEED_HREF)

        feed.entries.create(uid=TEST_ENTRY_UID,
                            title=TEST_ENTRY_TITLE,
                            link=TEST_ENTRY_LINK,
                            summary=TEST_ENTRY_SUMMARY,
                            publish_date=TEST_ENTRY_PUBLISH_DATE)
        self.assertRaises(feed.entries.create,
                          uid=TEST_ENTRY_UID,
                          title=TEST_FEED_TITLE,
                          link=TEST_ENTRY_LINK,
                          publish_date=TEST_ENTRY_PUBLISH_DATE)

    def test_tag(self):
        Tag.objects.create(name='tag')
        Tag.objects.create(name='Tag')
        self.assertRaises(Tag.objects.create, name='tag')
