import urllib.request
from django.http import HttpResponse
from bs4 import BeautifulSoup, Comment
import re


def tm_adder(matched_string):
    '''Adds the character'''
    return matched_string.group(1) + '™'


def remove_comments(text):
    '''Removes comments from Html'''
    return isinstance(text, Comment)


def func_checker(element):
    '''Checks element's tag'''
    if element.string is None:
        return True
    if element.name is None:
        return True
    if element.name == 'script':
        return True
    if element.name == 'style':
        return True

    return False


def replace(text):
    '''replaces string parts'''
    return re.sub(r'\b(\w{6})\b', tm_adder, text)


def link_retainer(link):
    '''Replaces given link with a 127.0.0.1 one'''
    if link['href'].find('habrahabr.ru') != -1:
        link['href'] = link['href'].replace('https://habrahabr.ru',
                                            'http://127.0.0.1:8000')


def proxy_view(request):
    '''Does proxy and filtering'''

    connection = urllib.request.Request("http://habrahabr.ru" + request.get_full_path())

    if request.method == "GET":
        content = urllib.request.urlopen(connection)
        headers = content.info()
        if headers['Content-Type'] == 'text/html; charset=UTF-8':
            soup = BeautifulSoup(content, 'html.parser')

            # Strip all the comments
            comments = soup.findAll(text=remove_comments)

            for comment in comments:
                comment.extract()

            elements = soup.body
            for child in elements.descendants:
                text = None
                if func_checker(child) is False:
                        text = child.string.strip()
                if text:
                    child.string.replace_with(replace(text))

            links = soup.findAll('a')
            for link in links:
                if 'href' in link.attrs.keys():
                    link_retainer(link)

            return HttpResponse(soup.prettify())
        else:
            return HttpResponse(content)

    if request.method == "POST":
        post = urllib.request.urlopen(connection, request.POST)
        return HttpResponse(post)
