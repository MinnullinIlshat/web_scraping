from urllib.request import urlopen 
from urllib.error import HTTPError, URLError
import pickle

url = 'https://www.pythonscraping.com/pages/page3.html'

try:
    html = urlopen(url)
except HTTPError as e:
    print(e)
except URLError as e:
    print(e)
else:
    with open('html_obj', 'w') as f:
        pickle.dump(html, f)