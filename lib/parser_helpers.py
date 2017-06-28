import bs4
from bs4 import BeautifulSoup
import json
from urllib.parse import urlencode
from urllib.request import urlopen
WIKI_API_URL = "https://wiki.archlinux.org/api.php"
OFF_SS_URL = "https://www.archlinux.org/packages/search/json/"
OFF_SI_URL = "https://www.archlinux.org/packages/"

def search (query):
    data = {"action": "parse", "format": "json",
            "page": query.lower (), "redirects": "resolve",
            "prop": "wikitext"}
    raw = urlopen (WIKI_API_URL, urlencode (data).encode ()).read ()
    answer = json.loads (raw)
    result = {'status': 0}
    if 'error' in answer:
        result['status'] = 1
        return result
    else:
        result['title'] = answer['parse']['title']
        result['text'] = mw.parse (answer['parse']['wikitext']['*'])

    return result

def get_section(page, number):
    result = dict ()
    data = {"action": "mobileview", "page": page, "sections": number,
            "format": "json", "noheadings": "nOheADinGs"}
    raw = urlopen (WIKI_API_URL, urlencode (data).encode ()).read ()
    answer = json.loads (raw)
    result['status'] = 0;
    
    if 'error' in answer: 
        result['status'] = 1
        return result
    elif len (answer['mobileview']['sections']) < number:
        result['status'] = 2
        return result

    result['title'] = page
    if 'normalizedtitle' in answer['mobileview']:
        result['title'] = answer['mobileview']['normalizedtitle']

    result['html'] = answer['mobileview']['sections'][number]['text']

    return result
#https://wiki.archlinux.org/api.php?action=mobileview&page=grub&sections=0&noheadings&format=rawfm&notransform

def extract_text (text):
    result = {'text': "", 'report': False}
    soup = BeautifulSoup (text, "lxml")
    for vege in soup.select ("p"):
        for child in vege.children:
            if type(child) is bs4.element.NavigableString:
                # FIXME
                if child == 'Related articles':
                    pass
                else:
                   result['text'] += child
            elif child.name is 'a':
                # [linktext](link)
                link = child['href']
                if link[0] is '/':
                    link = 'https://wiki.archlinux.org' + link
                result['text'] += "[" + child.string + "](" + link + ")"
            elif child.name is 'i':
                result['text'] += "_" + child.string + "_"
            else:
               result['report'] = True

    return result

def search_ss (name):
    result = {'status': 1, 'name': "", "description": "", "url": "",
            "repo": ""} 
    raw = urlopen (OFF_SS_URL + "?name=" + name).read ()
    answer = json.loads (raw)
    if len (result) < 1:
        return result
    else:
        result['status'] = 0
        result['name'] = answer['results'][0]['pkgname']
        result['url'] = answer['results'][0]['url']
        result['description'] = answer['results'][0]['pkgdesc']
        result['repo'] = answer['results'][0]['repo']
        
    return result
