import urllib.request
from django.http import HttpResponse
from bs4 import BeautifulSoup
import re


def tm_adder(matched_string):
    '''Adds the character'''
    return matched_string.group(1) + '™'


def proxy_view(request):
    '''Does proxy and filtering'''

    connection = urllib.request.Request("http://habrahabr.ru" + request.path)
    content = urllib.request.urlopen(connection)
    headers = content.info()

    if headers['Content-Type'] == 'text/html; charset=UTF-8':
        soup = BeautifulSoup(content, 'html.parser')

        for element in soup.find_all(text=True):
            text = element.string.strip()
            if text:
                if not element.find_parent('script') and \
                   not element.find_parent('head'):
                    element.replace_with(re.sub(r'\b(\w{6,})\b',
                                                tm_adder,
                                                text))

        return HttpResponse(soup.prettify())

    return HttpResponse(content)
