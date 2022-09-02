from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup 
import re 
import random 

pages = set()

#Retrieves a list of all Internal links found on a page 
def get_internal_links(bs, include_url):
    include_url = f'{urlparse(include_url).scheme}://{urlparse(include_url).netloc}'
    internal_links = []
    #Finds all links that begin with a "/"
    for link in bs.find_all('a', href=re.compile('^(/|.*'+include_url+')')):
        if (link_href:=link.attrs['href']) is not None:
            if link_href not in internal_links:
                if link_href.startswith('/'):
                    internal_links.append(include_url + link_href)
                else: 
                    internal_links.append(link_href)
    return internal_links 

#Retrieves a list of all external links found on a page
def get_external_links(bs, exclude_url):
    external_links = []
    #Finds all links that start with "http" that do
    #not contain the current URL
    for link in bs.find_all('a', href=re.compile('^(http|www)((?!'+exclude_url+').)*$')):
        if (link_href:=link.attrs['href']) is not None:
            if link_href not in external_links:
                external_links.append(link_href)
    return external_links 

def get_random_external_link(starting_page):
    html = urlopen(starting_page)
    bs = BeautifulSoup(html, 'html.parser')
    external_links = get_external_links(bs, urlparse(starting_page).netloc)
    if len(external_links) == 0:
        print('No external links, looking around the site for one')
        domain = f'{urlparse(starting_page).scheme}://{urlparse(starting_page).netloc}'
        internal_links = get_internal_links(bs, domain)
        return get_random_external_link(internal_links[random.randint(0,
                                        len(internal_links)-1)])
    return external_links[random.randint(0, len(external_links)-1)]

def follow_external_only(starting_site):
    external_link = get_random_external_link(starting_site)
    print(f'Random external link is: {external_link}')
    follow_external_only(external_link)

follow_external_only('http://oreilly.com')