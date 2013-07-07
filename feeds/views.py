# coding: utf-8
"""
===========
feeds.views
===========

Views for feeds application.

"""

from lxml import etree

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.middleware.csrf import get_token
from django.template.response import HttpResponse

from feeds.models import Feed, Tag
from users.models import UserFeed, UserTag


@login_required
@transaction.commit_on_success
def import_opml(request):
    user = request.user
    if request.POST and request.FILES and 'opml_file' in request.FILES:
        filename = request.FILES['opml_file'].temporary_file_path()

        parse_opml(filename, user)

    return HttpResponse('ok ' + get_token(request))


def parse_opml(filename, user):
    outlines_stack = []
    context = etree.iterparse(filename, events=("start", "end"), tag="outline")

    for action, elem in context:
        if action == 'start':
            parent = outlines_stack[-1] if outlines_stack else None
            if 'xmlUrl' not in elem.attrib:
                user_tag = add_tag(elem.attrib['title'], user, parent)
                outlines_stack.append(user_tag)
            else:
                user_feed = add_feed(
                    elem.attrib['title'], elem.attrib['xmlUrl'], user, parent
                )

                outlines_stack.append(user_feed)
        elif action == 'end':
            if outlines_stack:
                outlines_stack.pop()


def add_tag(name, user, parent):
    tag, created = Tag.objects.get_or_create(name=name)

    if created:
        tag.save()

    user_tag, created = UserTag.objects.get_or_create(
        tag=tag,
        user=user,
        parent=parent if parent else None
    )
    if created:
        user_tag.save()

    return user_tag


def add_feed(title, href, user, parent):
    feed, created = Feed.objects.get_or_create(
        title=title, href=href, link=href
    )

    if created:
        feed.save()

    user_feed, created = UserFeed.objects.get_or_create(
        feed=feed,
        user=user,
        parent=parent if parent else None,
    )
    if created:
        user_feed.save()

    return user_feed
