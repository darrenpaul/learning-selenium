import os
import random
import tempfile
from datetime import date

FOLLOWING_PATH = '{0}/configs/following.txt'.format(os.path.dirname(os.path.realpath(__file__)))

REMOVED_FOLLOWING_PATH = '{0}/configs/removed_following.txt'.format(
    os.path.dirname(os.path.realpath(__file__)))

VISITED_PATH = '{0}/configs/visted_urls.txt'.format(os.path.dirname(os.path.realpath(__file__)))

COMMENT_PATH = '{0}/configs/comments.txt'.format(os.path.dirname(os.path.realpath(__file__)))

GENERIC_COMMENT_PATH = '{0}/configs/generic_comments.txt'.format(
    os.path.dirname(os.path.realpath(__file__)))

TAGS_PATH = '{0}/configs/search_tags.txt'.format(os.path.dirname(os.path.realpath(__file__)))

CREDENTIALS_PATH = os.path.join(tempfile.gettempdir(), 'instagram_bot', 'credentials.txt')


def remove_all_followings():
    open(FOLLOWING_PATH, 'w+')


def add_following(user):
    if not os.path.exists(FOLLOWING_PATH):
        open(FOLLOWING_PATH, 'w+')
    with open(FOLLOWING_PATH, 'a') as doc:
        doc.write('{0}  {1}\n'.format(user, date.today()))


def get_following():
    followers = []
    with open(FOLLOWING_PATH) as doc:
        for line in doc.readlines():
            followers.append(line.strip())
    return followers


def add_removed_following(user):
    if not os.path.exists(REMOVED_FOLLOWING_PATH):
        open(REMOVED_FOLLOWING_PATH, 'w+')
    with open(REMOVED_FOLLOWING_PATH, 'a') as doc:
        doc.write('{0}  {1}\n'.format(user, date.today()))


def get_removed_following():
    followers = []
    with open(REMOVED_FOLLOWING_PATH) as doc:
        for line in doc.readlines():
            followers.append(line.strip())
    return followers


def add_visted_urls(url):
    with open(VISITED_PATH, 'a') as doc:
        doc.write('{0}\n'.format(url))


def get_visted_urls():
    urls = []
    if not os.path.exists(VISITED_PATH):
        open(VISITED_PATH, 'w+')

    with open(VISITED_PATH) as doc:
        for line in doc.readlines():
            urls.append(r'{0}'.format(line.strip()))
    return urls


def get_comment():
    comments = []
    with open(COMMENT_PATH) as doc:
        for line in doc.readlines():
            comments.append('{0}'.format(line))

    random_index = random.randint(0, len(comments)-1)
    comment = comments[random_index]
    return comment


def get_generic_comment():
    comments = []
    with open(GENERIC_COMMENT_PATH) as doc:
        for line in doc.readlines():
            comments.append('{0}'.format(line))

    random_index = random.randint(0, len(comments)-1)
    comment = comments[random_index]
    return comment


def get_search_tags():
    tags = []
    with open(TAGS_PATH) as doc:
        for line in doc.readlines():
            tags.append('{0}'.format(line))
    return tags


def get_user_credentials():
    directory = os.path.dirname(CREDENTIALS_PATH)
    email = ''
    password = ''
    if not os.path.exists(directory):
        os.mkdir(directory)

    if not os.path.exists(CREDENTIALS_PATH):
        print('Unable to find credentials please enter them.')
        raw_input_email = input('Please enter your email address for instagram: ')
        raw_input_password = input('Please enter your password for instagram: ')
        with open(CREDENTIALS_PATH, 'w+') as doc:
            doc.write('{0}  {1}\n'.format(raw_input_email.strip(), raw_input_password.strip()))
    with open(CREDENTIALS_PATH) as doc:
        for line in doc.readlines():
            email, password = line.split('  ')
    return {'email': email, 'password': password}


def remove_credentials():
    if os.path.exists(CREDENTIALS_PATH):
        os.remove(CREDENTIALS_PATH)
