# -*- coding: utf-8 -*-
import os
import shutil
import logging
import zipfile
import pandas as pd
from dotenv import find_dotenv, load_dotenv
from process import process_df

def get_directories():
    root_dir = os.path.dirname(os.path.abspath(__file__)).split('/')[:-2]
    root_dir = '/'.join(root_dir)

    raw_dir = os.path.join(root_dir, 'data/raw')
    interim_dir = os.path.join(root_dir, 'data/interim')
    processed_dir = os.path.join(root_dir, 'data/processed')

    return raw_dir, interim_dir, processed_dir

def main():
    """ Extracts zipped contents into interim, then after further modifications it saved into
        cleaned data ready to be analyzed (saved in ../processed).
    """

    # Getting the paths correctly for the folders needed.
    raw_dir, interim_dir, processed_dir = get_directories()

    logger = logging.getLogger(__name__)
    logger.info('Unzipping files into the interim folder')

    # obtaining the zipped original version and unzipping into new folder
    zip_ref = zipfile.ZipFile(os.path.join(raw_dir, SOURCE_FILENAME), 'r')
    zip_ref.extractall(interim_dir)
    try:
        os.rmdir(os.path.join(interim_dir, '__MACOSX'))
    except FileNotFoundError:
        None # Not unzipping on OSX


    # Now we'll take the preprocessed files and add columns, remove the not-needed columns
    logger.info('making final data set from raw data')

    # Using the column mapping provided with the documentation
    columns = ['age','class of worker','detailed industry recode','detailed occupation recode','education',
               'wage per hour','enroll in edu inst last wk','marital stat','major industry code',
               'major occupation code','race','hispanic origin','sex','member of a labor union',
               'reason for unemployment','full or part time employment stat','capital gains','capital losses',
               'dividends from stocks','tax filer stat','region of previous residence','state of previous residence',
               'detailed household and family stat','detailed household summary in household',
               'instance weight','migration code-change in msa','migration code-change in reg',
               'migration code-move within reg','live in this house 1 year ago','migration prev res in sunbelt',
               'num persons worked for employer','family members under 18','country of birth father',
               'country of birth mother','country of birth self','citizenship','own business or self employed',
               "fill inc questionnaire for veteran's admin",'veterans benefits','weeks worked in year','year',
               'salary']


    # Process and remove column from training and test sets
    df = pd.read_csv(interim_dir + '/us_census_full/census_income_learn.csv', names=columns)
    df = df.drop(columns=['instance weight'])
    df.to_csv(interim_dir + '/census_income_learn.csv', index=False)

    df = pd.read_csv(interim_dir + '/us_census_full/census_income_test.csv', names=columns)
    df = df.drop(columns=['instance weight'])
    df.to_csv(interim_dir + '/census_income_test.csv', index=False)

    shutil.rmtree(os.path.join(interim_dir, 'us_census_full'))

    df_train, df_test = process_df(interim_dir)
    df_train.to_csv(interim_dir + '/preprocessed_train.csv', index=False)
    df_test.to_csv(interim_dir + '/preprocessed_test.csv', index=False)



if __name__ == '__main__':
    load_dotenv(find_dotenv())
    SOURCE_FILENAME = os.getenv("SOURCE_URL").split('/')[-1]
    main()
