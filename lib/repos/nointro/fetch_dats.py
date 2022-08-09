#!/bin/env python3

import os
import sys
from concurrent.futures import ThreadPoolExecutor
if not os.getcwd() in sys.path:
    sys.path.append(os.getcwd())
from lib.repos.nointro.download import download_daily

TMP = 'tmp'
TMP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../../{TMP}'))
TMP_NOINTRO = os.path.join(TMP_DIR, 'nointro')
TMP_DATS = os.path.join(TMP_NOINTRO, 'dats')
MAIN_URL = 'http://datomatic.org'


def mktmpdirs():
    os.makedirs(TMP_DIR, exist_ok=True)
    os.makedirs(TMP_NOINTRO, exist_ok=True)
    os.makedirs(TMP_DATS, exist_ok=True)


def clean():
    # delete old files
    os.system(f'rm -rf {TMP_NOINTRO}/dats/*')


def main():
    def download_dats(file):
        download_daily()

    os.system(f'cd {TMP_DATS} && cp ../*.zip . && unzip -o \'*.zip\' && rm *.zip')
    os.system(f'cd {TMP_NOINTRO} && mv *.zip history/')

    # zip files in TMP_DIR with 7z
    print('Zipping files')
    os.system(f'cd {TMP_DIR} && 7z a -tzip nointro.zip nointro/dats')


if __name__ == '__main__':
    mktmpdirs()
    clean()
    main()
