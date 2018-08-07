#!/usr/bin/env python
"""
coding=utf-8

Code Template

"""
import datetime
import logging
import time

import pandas
import praw

import lib


def scrape_subreddit(subreddit_name):
    # TODO Docstring

    logging.info('Beginning Reddit scraper, for subreddit: {}'.format(subreddit_name))

    # Reference variables
    parsed_submission_agg = list()

    # Create connection. For details, see https://www.reddit.com/prefs/apps/

    logging.info('Creating reddit connection')
    reddit = praw.Reddit(client_id=lib.get_conf('client_id'),
                         client_secret=lib.get_conf('client_secret'),
                         user_agent='upvote_estimator:0.0.1')

    # Find correct subreddit
    logging.info('Searching for subreddit: {}'.format(subreddit_name))
    subreddit = reddit.subreddit(subreddit_name)
    logging.debug('Searched for subreddit: {}, found subreddit: {}, {}'.format(subreddit_name, subreddit.display_name, subreddit.title))

    # Iterate through posts chronologically
    for index, submission in enumerate(subreddit.new(limit=1000)):
        logging.info('Working number {}, submission: {}'.format(index, submission))

        # Parse each submission and extract essential fields
        parsed_submission = submission_parser(submission)

        # Add info from each post to aggregator
        parsed_submission_agg.append(parsed_submission)

        if lib.get_conf('test_run') and index >= 49:
            break
    # Create DataFrame from pulled data
    posts = pandas.DataFrame(parsed_submission_agg)

    # Return
    return posts


def submission_parser(submission):
    # Reference variables
    agg = dict()

    fields = ['author', 'spoiler', 'over_18', 'url', 'id', 'name', 'subreddit_name_prefixed', 'score', 'ups', 'downs', 'likes', 'num_comments', 'title', 'selftext']
    for field in fields:
        value = submission.__dict__.get(field, None)

        try:
            agg[field] = unicode(value).encode('ascii', errors='ignore') if value is not None else None

        except:
            agg[field] = None
            logging.warn('Issue encoding field: {}, for submission: {}'.format(field, submission))

    return agg