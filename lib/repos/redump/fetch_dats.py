#!/bin/env python3

from html.parser import HTMLParser
import urllib.request
import os
from concurrent.futures import ThreadPoolExecutor

TMP = 'tmp'
TMP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../../{TMP}'))
TMP_REDUMP = os.path.join(TMP_DIR, 'redump')
TMP_DATS = os.path.join(TMP_REDUMP, 'dats')
MAIN_URL = 'http://redump.org'
DOWNLOAD_URL = 'http://redump.org/downloads/'
TYPES = ["datfile", "cues", "gdi", "sbi"]


def mktmpdirs():
    os.makedirs(TMP_DIR, exist_ok=True)
    os.makedirs(TMP_REDUMP, exist_ok=True)
    os.makedirs(TMP_DATS, exist_ok=True)

def clean():
    # delete old files
    os.system(f'rm -rf {TMP_REDUMP}/*')


class MyHTMLParser(HTMLParser):
    rootpath = MAIN_URL
    types = TYPES

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            taga = dict(attrs)
            if 'href' in taga:
                href = taga['href']
                hrefsplit = href.split('/')
                if len(hrefsplit) > 1 and hrefsplit[1] in self.types:
                    output = hrefsplit[1]
                    if 'bios' in href:
                        output = 'bios'
                    savefile(output, self.rootpath+href)


def savefile(output, href):
    with open(os.path.join(TMP_REDUMP, f'{output}.txt'), 'a+') as fp:
        fp.write(href+"\n")


def main():
    def download_dats(file):
        new_path = os.path.join(TMP_DATS, file)
        os.makedirs(new_path, exist_ok=True)
        os.system(f'cd {new_path} && aria2c --file-allocation=prealloc -i ../../{file}.txt')
        # extract dat files
        if file in ['datfile']:
            os.system(f'cd {new_path} && unzip -o \'*.zip\'')
            os.system(f'cd {new_path} && rm *.zip')

    red = urllib.request.urlopen(DOWNLOAD_URL)

    redumphtml = red.read()

    print('Parsing Redump HTML')
    parser = MyHTMLParser()
    parser.feed(str(redumphtml))

    print('Downloading new dats')
    NEWTYPES = TYPES+['bios']

    with ThreadPoolExecutor(max_workers=10) as executor:
        for file in NEWTYPES:
            executor.submit(download_dats, file)

    # zip files in TMP_DIR with 7z
    print('Zipping files')
    os.system(f'cd {TMP_DIR} && 7z a -tzip redump.zip redump')

if __name__ == '__main__':
    mktmpdirs()
    clean()
    main()
