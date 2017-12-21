import certifi
import urllib3

from pyquery import PyQuery
from uritools import urisplit

import json
import os.path

def urlToId(url):
    return urisplit(url).path.split('/')[1]

def menuEntryToDict(e):
    url = PyQuery(e).attr.href
    title = PyQuery(e).text()
    return { 
            'href': url,
            'id': urlToId(url),
            'title': title 
            }
    

def menuListToDict(page):
    categoryList = PyQuery(page)('ul#mega-menu-info_nav').find('a')
    return [menuEntryToDict(e) for e in categoryList]

def generateCategoryFiles():
    with urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where()) as http:
        baseUrl = 'https://mediabiasfactcheck.com/'
        homepage = http.request('GET', baseUrl).data
    categories = [ d
        for d in menuListToDict(homepage)
        if 'Search' not in d['title'] ]
    standardCategories = [ d 
        for d in categories 
        if 'Bias' in d['title'] ]
    otherCategories = [ d
        for d in categories
        if d not in standardCategories ]
    for category in ['standardCategories', 'otherCategories']:
        categoryJSON = json.dumps(eval(category), sort_keys=True, indent=2)
        categoryFilePath = os.path.join('dist', category + '.json')
        with open(categoryFilePath, 'w') as categoryFile:
            categoryFile.write(categoryJSON)


