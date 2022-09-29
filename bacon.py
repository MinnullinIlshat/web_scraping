import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import psycopg2 
from random import shuffle 

conn = psycopg2.connect('dbname=wikipedia user=ilshat')
cur = conn.cursor()

def insert_page_if_not_exists(url):
    cur.execute(f'SELECT * FROM pages WHERE url = \'{url}\'')
    if cur.rowcount == 0:
        cur.execute(f'INSERT INTO pages (url) VALUES (\'{url}\')')
        conn.commit() 
        return cur.lastrowid 
    else: 
        return cur.fetchone()[0]

def load_pages():
    cur.execute('SELECT * FROM pages')
    pages = [row[1] for row in cur.fetchall()]
    return pages 

def insert_link(from_page_id, to_page_id):
    cur.execute(f'SELECT * FROM links WHERE from_page_id = {from_page_id} '
        f'AND to_page_id = {to_page_id}')
    if cur.rowcount == 0:
        cur.execute('INSERT INTO links (from_page_id, to_page_id) VALUES'
            f' ({int(from_page_id)}, {int(to_page_id)})')
        conn.commit() 

def get_links(page_url, recursion_level, pages):
    if recursion_level > 4:
        return 
    
    page_id = insert_page_if_not_exists(page_url)
    html = urlopen(f'https://en.wikipedia.org{page_url}')
    bs = BeautifulSoup(html.read(), 'html.parser')
    links = bs.find_all('a', href=re.compile(r'^(/wiki/)((?!:).)*$'))
    links = [link.attrs['href'] for link in links]

    for link in links:
        insert_link(page_id, insert_page_if_not_exists(link))
        if link not in pages:
            pages.append(link)
            get_links(link, recursion_level+1, pages)
        
get_links('/wiki/Kevin_Bacon', 0, load_pages())
cur.close() 
conn.close()