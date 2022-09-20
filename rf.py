import os 
from urllib.request import urlretrieve, urlopen 
from bs4 import BeautifulSoup 

download_directory = 'downloaded'
base_url = 'https://pythonscraping.com'

def get_absolute_url(base_url, source):
    if source.startswith('https://www.'):
        url = f'https://{source[12:]}'
    elif source.startswith('https://'):
        url = source 
    elif source.startswith('www.'):
        url = source[4:]
        url = f'https://{source}'
    else: 
        url = f'{base_url}/{source}'
    return url if base_url in url else None

def get_download_path(base_url, absolute_url, download_directory):
    path = absolute_url.replace('www.', '')
    path = path.replace(base_url, '')
    path = download_directory + path 
    directory = os.path.dirname(path)

    if not os.path.exists(directory):
        os.makedirs(directory)

    return path 

if __name__ == '__main__':
    html = urlopen('https://pythonscraping.com/')
    bs = BeautifulSoup(html, 'html.parser')

    download_list = bs.find_all(src=True)

    for download in download_list:
        file_url = get_absolute_url(base_url, download['src'])
        if file_url:
            print(file_url)
        
            urlretrieve(file_url, get_download_path(base_url, file_url, download_directory))