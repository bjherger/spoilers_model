#!/usr/bin/env python
"""
coding=utf-8

Code Template

"""
import logging
import os

import pandas
from keras.callbacks import TensorBoard, ModelCheckpoint

import lib
import models
from reddit_scraper import scrape_subreddit


def main():
    """
    Main function documentation template
    :return: None
    :rtype: None
    """
    logging.basicConfig(level=logging.INFO)

    logging.info('Beginning batch: {}'.format(lib.get_batch_name()))

    if lib.get_conf('new_data_pull'):
        observations = extract()
        observations.to_feather(lib.get_conf('raw_observations_feather_path'))

    observations = pandas.read_feather(lib.get_conf('raw_observations_feather_path'))
    observations, X, y = transform(observations)
    model(observations, X, y)
    load()
    pass


def extract():
    logging.info('Begin extract')

    observations = scrape_subreddit(lib.get_conf('subreddit'))

    logging.info('End extract')
    lib.archive_dataset_schemas('extract', locals(), globals())
    return observations


def transform(observations):
    logging.info('Begin transform')

    if lib.get_conf('test_run'):
        logging.info('Sample run, selecting random sub-sample of observations')
        observations = observations.sample(n=1000).copy()
    logging.info('Utilizing {} observations'.format(len(observations.index)))

    # Create modeling text
    observations['modeling_text'] = observations['title'] + ' ' + observations['selftext']
    observations['spoiler'] = observations['spoiler'].apply(eval)

    X, y = lib.gen_x_y(observations['modeling_text'], observations['spoiler'])

    logging.info('Spoilers: {}. Observations: {}'.format(sum(observations['spoiler']), len(observations.index)))

    lib.archive_dataset_schemas('transform', locals(), globals())
    logging.info('End transform')
    return observations, X, y


def model(observations, X, y):
    logging.info('Begin model')

    # Set up callbacks
    tf_log_path = os.path.join(os.path.expanduser('~/log_dir'), lib.get_batch_name())
    logging.info('Using Tensorboard path: {}'.format(tf_log_path))

    mc_log_path = os.path.join(lib.get_conf('model_checkpoint_path'),
                               lib.get_batch_name() + '_epoch_{epoch:03d}_val_loss_{val_loss:.2f}.h5py')
    logging.info('Using mc_log_path path: {}'.format(mc_log_path))
    callbacks = [TensorBoard(log_dir=tf_log_path),
                 ModelCheckpoint(mc_log_path)]

    # Create model
    bool_model = models.bi_lstm_embedding(X, y)

    # Fit model
    bool_model.fit(X, y, callbacks=callbacks, validation_split=.2, epochs=lib.get_conf('num_epochs'), batch_size=512)

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
