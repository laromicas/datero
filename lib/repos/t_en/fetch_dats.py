#!/bin/env python3

import os
from concurrent.futures import ThreadPoolExecutor
import sys

if not os.getcwd() in sys.path:
    sys.path.append(os.getcwd())

from lib.repositories.ia import InternetArchive


TMP = 'tmp'
TMP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../../{TMP}'))
TMP_T_EN = os.path.join(TMP_DIR, 't-en')
TMP_DATS = os.path.join(TMP_T_EN, 'dats')


MAIN_URL = 'http://archive.org'
ARCHIVE_URL = 'En-ROMs'
DAT_FOLDER = 'DATs'

def get_archive_item(url):
    return url.split('/')[-1]

def mktmpdirs():
    os.makedirs(TMP_DIR, exist_ok=True)
    os.makedirs(TMP_T_EN, exist_ok=True)
    os.makedirs(TMP_DATS, exist_ok=True)

def clean():
    # delete old files
    os.system(f'rm -rf {TMP_T_EN}/*')


def main():
    os.makedirs(TMP_DATS, exist_ok=True)
    def download_dats(download_path, file):
        url = os.path.join(download_path, file)
        os.system(f'cd {TMP_DATS} && aria2c --file-allocation=prealloc "{url}"')

    print('Fetching Archive.org DAT files')
    ia = InternetArchive(ARCHIVE_URL)

    print('Downloading new dats')

    with ThreadPoolExecutor(max_workers=10) as executor:
        for file in ia.files_from_folder("DATs"):
            executor.submit(download_dats, ia.get_download_path(), file['name'])

    os.system(f'cd {TMP_DATS} && unzip -o \'*.zip\'')
    os.system(f'cd {TMP_DATS} && rm *.zip')

    # zip files in TMP_DIR with 7z
    print('Zipping files')
    os.system(f'cd {TMP_DIR} && 7z a -tzip t-en.zip t-en')

if __name__ == '__main__':
    mktmpdirs()
    clean()
    main()
