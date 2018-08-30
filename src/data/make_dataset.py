# -*- coding: utf-8 -*-
import os
import logging
import zipfile
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

def main():
    """ Extracts zipped contents into interim, then after further modifications it saved into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)

    # obtaining the zipped original version and unzipping into new folder
    logger.info('Unzipping files into the interim folder')
    zip_ref = zipfile.ZipFile('../../data/raw/{}'.format(SOURCE_FILENAME), 'r')
    zip_ref.extractall('../../data/interim/')
    try:
        os.rmdir('../../data/interim/' + '__MACOSX')
    except FileNotFoundError:
        None # Not unzipping on OSX

    logger.info('making final data set from raw data')


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    SOURCE_FILENAME = os.getenv("SOURCE_URL").split('/')[-1]
    main()
