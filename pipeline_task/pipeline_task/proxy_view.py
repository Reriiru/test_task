import urllib.request
import urllib.error 
import re
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import View
from bs4 import BeautifulSoup, Comment


class ProxyView(View):

    def tm_adder(self, matched_string):
        '''Adds the character'''
        return matched_string.group(1) + '™'

    def remove_comments(self, text):
        '''Removes comments from Html'''
        return isinstance(text, Comment)

    def tag_checker(self, element):
        '''Checks element's tag'''
        if element.name == 'script':
            return False
        if element.name == 'style':
            return False

        return True

    def replace(self, text):
        '''replaces string parts'''
        return re.sub(r'\b(\w{6})\b', self.tm_adder, text)

    def link_retainer(self, link):
        '''Replaces given link with a 127.0.0.1 one'''
        if link['href'].find('habrahabr.ru') != -1:
            link['href'] = link['href'].replace('https://habrahabr.ru',
                                                'http://127.0.0.1:8000')

    def document_changer(self, bs):
        elements = bs.body.find_all("", text=True)

        comments = bs.findAll(text=self.remove_comments)

        for comment in comments:
            comment.extract()

        elements = bs.body.find_all(text=True)

        for child in elements:
            if self.tag_checker(child.parent):
                text = None
                if child.string:
                    text = child.string.strip()
                if text:
                    child.replace_with(self.replace(text))

        links = bs.findAll('a')

        for link in links:
            if 'href' in link.attrs.keys():
                self.link_retainer(link)
        
        return bs

    def get(self, request, **kwargs):
        '''Does proxy and filtering'''

        connection = urllib.request.Request("http://habrahabr.ru"
                                            + request.get_full_path())
        
        try:
            content = urllib.request.urlopen(connection)
        except urllib.error.HTTPError as error:
            return HttpResponse('Error! Code: 404', status=404)

        headers = content.info()
            
        # Preserve the redirects so we don't have to proxy everything
        if content.geturl().split('/')[2] != 'habrahabr.ru':
            return redirect(content.geturl())

        # Check if we actually try to parse html and not binary or js.
        if headers['Content-Type'] == 'text/html; charset=UTF-8':

            soup = BeautifulSoup(content, 'html5lib')

            soup = self.document_changer(soup)

            return HttpResponse(soup.prettify())
        else:
            return HttpResponse(content)

    def post(self, request, **kwargs):
        # We just pass all the post requests as is to habrahabr.
        connection = urllib.request.Request("http://habrahabr.ru"
                                            + request.get_full_path())
        post = urllib.request.urlopen(connection, request.POST)
        return HttpResponse(post)
