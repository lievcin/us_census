# -*- coding: utf-8 -*-
import os
import logging
import urllib.request
from dotenv import find_dotenv, load_dotenv


def main():
		""" Fetch data from source and store in raw folder
		"""
		logger = logging.getLogger(__name__)
		logger.info('going for the data...')
		urllib.request.urlretrieve(SOURCE_URL, '../../data/raw/{}'.format(SOURCE_FILENAME))

if __name__ == '__main__':
		load_dotenv(find_dotenv())

		SOURCE_URL = os.getenv("SOURCE_URL")
		SOURCE_FILENAME = SOURCE_URL.split('/')[-1]

		main()