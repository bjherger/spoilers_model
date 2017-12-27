#!/usr/bin/env python
"""
coding=utf-8

Code Template

"""
import logging

import pandas

import lib
from reddit_scraper import scrape_subreddit


def main():
    """
    Main function documentation template
    :return: None
    :rtype: None
    """
    logging.basicConfig(level=logging.INFO)

    if lib.get_conf('new_data_pull'):
        observations = extract()
        observations.to_feather(lib.get_conf('raw_observations_feather_path'))

    observations = pandas.read_feather(lib.get_conf('raw_observations_feather_path'))
    transform(observations)
    model()
    load()
    pass


def extract():
    logging.info('Begin extract')

    observations = scrape_subreddit(lib.get_conf('subreddit'), lib.get_conf('history_num_days'))

    logging.info('End extract')
    lib.archive_dataset_schemas('extract', locals(), globals())
    return observations


def transform(observations):
    logging.info('Begin transform')

    if lib.get_conf('test_run'):
        logging.info('Sample run, selecting random sub-sample of observations')
        observations = observations.sample(n=150).copy()

    # Create modeling text
    observations['modeling_text'] = observations['title'] + ' ' + observations['selftext']
    observations['spoiler'] = observations['spoiler'].apply(eval)

    x, y = lib.gen_x_y(observations['modeling_text'], observations['spoiler'])

    logging.info('Spoilers: {}. Observations: {}'.format(sum(observations['spoiler']), len(observations.index)))

    lib.archive_dataset_schemas('transform', locals(), globals())
    logging.info('End transform')
    pass


def model():
    logging.info('Begin model')

    lib.archive_dataset_schemas('model', locals(), globals())
    logging.info('End model')
    pass


def load():
    logging.info('Begin load')

    lib.archive_dataset_schemas('load', locals(), globals())
    logging.info('End load')
    pass


# Main section
if __name__ == '__main__':
    main()
