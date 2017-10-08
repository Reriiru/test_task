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


def func_checker(elment):
    if element.find_parent('script') and \
       element.find_parent('style'):
        return True
    else:
        return False


def proxy_view(request):
    '''Does proxy and filtering'''

    connection = urllib.request.Request("http://habrahabr.ru" + request.path)
    content = urllib.request.urlopen(connection)
    headers = content.info()

    if headers['Content-Type'] == 'text/html; charset=UTF-8':
        soup = BeautifulSoup(content, 'html.parser')

        comments = soup.findAll(text=remove_comments)

        for comment in comments:
            if not func_checker(comment):
                comment.extract()

        elements = soup.body.find_all(text=True)
        print(soup.body.find_all())
        for element in elements:
            text = None
            if not func_checker(element):
                text = element.string.strip()
            if text:
                element.replace_with(re.sub(r'\b(\w{6})\b',
                                            tm_adder,
                                            text))

        return HttpResponse(soup.prettify())

    return HttpResponse(content)
