import json
import os

from django.core import management
from django.core.management.base import BaseCommand, CommandError
from django.core.management.commands import loaddata
from faker import Faker
from faker.generator import random
from lorem import get_paragraph, get_sentence, get_word


# CONSTANTS
POSTS_NUMBER = 100
COMMENTS_NUMBER = 100


def generate_post() -> dict:
    """
    Generate random post
    @return: dict with title, short_description, image,
             full_description, user, posted
    """
    dict_post = {
        'title': '',
        'short_description': '',
        'image': '',
        'full_description': '',
        'user': 1,
        'posted': False
    }
    fake = Faker(['en_US'])
    dict_post['title'] = get_word(count=1)
    dict_post['short_description'] = get_sentence(count=1,
                                                  word_range=(4, 8),
                                                  sep=' ')
    dict_post['image'] = fake.image_url()
    dict_post['full_description'] = get_paragraph(count=3,
                                                  comma=(0, 2),
                                                  word_range=(4, 8),
                                                  sentence_range=(5, 10),
                                                  sep=os.linesep)
    dict_post['user'] = random.randint(1, 2)
    dict_post['posted'] = random.choice([True, False])
    return dict_post


def generate_comment() -> dict:
    """
    Generate random post
    @return: dict with title, short_description, image,
             full_description, user, posted
    """
    dict_comment = {
        'username': '',
        'text': '',
        'post': 1,
        'moderated': False
    }
    fake = Faker(['en_US'])
    dict_comment['username'] = fake.first_name()
    dict_comment['text'] = get_sentence(count=1,
                                        word_range=(4, 8),
                                        sep=' ')
    dict_comment['post'] = random.randint(1, POSTS_NUMBER)
    dict_comment['moderated'] = random.choice([True, False])
    return dict_comment


class Command(BaseCommand):
    help = "Create random posts and comments"  # noqa:A003

    def handle(self, *args, **kwargs):

        # Generate base of posts to json file for loaddata
        posts_base = []
        for n in range(1, POSTS_NUMBER + 1):
            post = generate_post()
            post_instance = {
                "model": "posts.post",
                "pk": n,
                "fields": {
                    "title": post['title'],
                    "short_description": post['short_description'],
                    "image": post['image'],
                    "full_description": post['full_description'],
                    "user": post['user'],
                    "posted": post['posted'],
                }
            }
            posts_base.append(post_instance)
        try:
            with open('posts/fixtures/posts_post.json', 'w') as posts:
                json.dump(posts_base, posts)
        except Exception as err:
            raise CommandError('Some error occurred:', str(err))

        # Generate base of comments to json file for loaddata
        comments_base = []
        for n in range(1, COMMENTS_NUMBER + 1):
            comment = generate_comment()
            comment_instance = {
                "model": "posts.comment",
                "pk": n,
                "fields": {
                    "username": comment['username'],
                    "text": comment['text'],
                    "post": comment['post'],
                    "moderated": comment['moderated'],
                }
            }
            comments_base.append(comment_instance)
        try:
            with open('posts/fixtures/posts_comment.json', 'w') as comments:
                json.dump(comments_base, comments)
        except Exception as err:
            raise CommandError('Some error occurred:', str(err))

        # Load to base
        management.call_command(loaddata.Command(), 'posts_post.json', verbosity=0)
        management.call_command(loaddata.Command(), 'posts_comment.json', verbosity=0)
