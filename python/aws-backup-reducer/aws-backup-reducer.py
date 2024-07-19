#!/usr/bin/env python3.12

import argparse
import boto3
import logging

from datetime import datetime, timedelta, UTC
from itertools import batched, groupby

def delete_old_objects(
    bucket: str,
    prefix: str = '',
    days_to_retain_all_objects: int = 30,
    interactive: bool = True,
    dry_run: bool = True,
    delete_batch_size: int = 1000,
    delete_quietly: bool = False,
    log_level: str = 'WARN',
):

    """
    Delete old objects from an AWS S3 bucket

    Retain days_to_retain_all_objects days worth of objects, then 1 per week for 1 year, then 1 per year

    FIXME: check the bucket is not a _directory bucket_
    """

    assert bucket != '', 'bucket cannot be an empty string'
    assert delete_batch_size >=1 and delete_batch_size <= 1000, 'delete_batch_size must be between 1 and 1000'

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.getLevelName(log_level.upper()))
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.debug(vars())

    if prefix == '':
        logger.warning('No prefix given, this will operate on the entire bucket')

    actionable_limit_date = datetime.now(UTC) - timedelta(days=days_to_retain_all_objects)
    logger.info(f'acting on objects last modified before {actionable_limit_date.strftime(format='%F at %T')}')

    # get all objects
    # the client uses pagination, requiring to use the paginator
    # => the paginator returns a generator, and should one run through it it will be spent
    # => save the paginator's results to a flattened list
    client = boto3.client('s3')
    paginator = client.get_paginator('list_objects_v2')
    iterator = paginator.paginate(
        Bucket = bucket,
        Prefix = prefix,
    )
    objects = []
    for obj in iterator:
        objects.extend(obj['Contents'])
    logger.info(f'found {len(objects)} objects')
    logger.debug(f'objects: {objects}')
    # sorting by date will make things easier later
    objects.sort(key=lambda obj:obj['LastModified'])
    logger.info(f'objects sorted by last modified date (older to newer)')
    logger.debug(f'sorted objects: {objects}')

    # lock the original list of objects down
    # I do know my chickens
    objects = tuple(objects)

    # filter out directories
    actionable_objects = [obj for obj in objects if not obj['Key'].endswith('/')]
    logger.info(f'found {len(actionable_objects)} actionable objects')
    logger.debug(f'actionable objects: {actionable_objects}')

    # filter out objects last modified in the last x days to keep
    # filtering from the iterator using iterator.search and a jmespath query would have been the easiest option
    # … but yeah, jmespath queries, thanks but nah thanks
    actionable_objects = [obj for obj in actionable_objects if obj['LastModified'] < actionable_limit_date]
    logger.info(f'filtered out objects modified in the last {days_to_retain_all_objects} days')
    logger.info(f'actionable objects reduced to {len(actionable_objects)}')
    logger.debug(f'actionable objects: {actionable_objects}')

    # filter out 1 object per year to keep
    # objects are ordered from the oldest to the most recent => grouping by year, the latest in each group set will be
    # the one to keep
    for k, v in groupby(actionable_objects, key = lambda obj: obj['LastModified'].isocalendar().year):
        objects_by_year = list(v)
        actionable_objects.remove(objects_by_year[-1])
        logger.info(f'filtered out object to keep for year {k}')
        logger.debug(f'filtered out object: {objects_by_year[-1]}')
    logger.info(f'actionable objects reduced to {len(actionable_objects)}')
    logger.debug(f'actionable objects: {actionable_objects}')

    # filter out 1 object per week to keep
    # the requirement being 1y, no need to do this per year *and*, per week
    # grouping by week, the latest in each group set will be the one to keep
    for k, v in groupby(actionable_objects, key = lambda obj: obj['LastModified'].isocalendar().week):
        objects_by_week = list(v)
        actionable_objects.remove(objects_by_week[-1])
        logger.info(f'filtered out object to keep for week {k}')
        logger.debug(f'filtered out object: {objects_by_week[-1]}')
    logger.info(f'actionable objects reduced to {len(actionable_objects)}')
    logger.debug(f'actionable objects: {actionable_objects}')

    # lock the list of actionable objects down
    # I do know my chickens
    actionable_objects = tuple(actionable_objects)
    logger.debug(f'retained objects: {[obj for obj in objects if obj not in actionable_objects]}')

    # use one bulk request, it makes no sense to call it once per object
    # bulk requests can sustain up to 1000 objects at a time => send requests with batches
    for batch in batched(actionable_objects, delete_batch_size):
        if interactive:
            print(f'About to {"faking" if dry_run else "really"} delete {len(batch)} objects.')
            proceed = input('Proceed?\n> ')
            if proceed.lower() not in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']:
                print(f'Batch skipped')
                continue
        if dry_run:
            logger.info(f'faked deleting {len(batch)} objects')
            logger.debug(f'supposedly deleted objects: {batch}')
        else:
            response = client.delete_objects(
                Bucket = bucket,
                Delete = {
                    'Objects': [{'Key':_['Key']} for _ in actionable_objects],
                    'Quiet': delete_quietly,
                },
            )
            logger.debug(f'response: {response}')
            logger.info(f'deletion returned code {response['ResponseMetadata']['HTTPStatusCode']}')
            logger.warning(f'deleted {len(response['Deleted'])} objects')
            logger.debug(f'deleted objects: {response['Deleted']}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Delete old data from an AWS S3 bucket')
    parser.add_argument('bucket', type=str, help='Bucket containing the data; required')
    parser.add_argument(
        '-p', '--prefix', type=str, default='',
        help='Prefix for the data in the bucket; defaults to "", suggested if using prefixes',
    )
    parser.add_argument(
        '-d', '--retain-days', type=int, default=30,
        help='Number of days to retain objects for; defaults to 30',
    )
    interactivity = parser.add_mutually_exclusive_group()
    interactivity.add_argument(
        '-i', '--interactive', action='store_true', default=True,
        help='Be interactive; defaults to false',
    )
    interactivity.add_argument(
        '-I', '--no-interactive', dest='interactive', action='store_false',
        help='Do *not* be interactive',
    )
    run_type = parser.add_mutually_exclusive_group()
    run_type.add_argument('--dry-run', action='store_true', default=True, help='Dry run; defaults to true')
    run_type.add_argument('--no-dry-run', dest='dry_run', action='store_false', default=True, help='Do *not* dry run')
    parser.add_argument(
        '-s', '--delete-batch-size', type=int, default=1000,
        help='Number of objects to request or delete at any time; min 1, max 1000, defaults to 1000',
    )
    parser.add_argument(
        '-q', '--delete-quietly', action='store_true', default=False,
        help='Delete quietly; defaults to false',
    )
    parser.add_argument('-l', '--log-level', type=str, default='WARN', help='Log level name; defaults to "WARN"')
    args = parser.parse_args()

    # delete_old_objects(
    #     bucket = args.bucket,
    #     prefix = args.prefix,
    #     days_to_retain_all_objects = args.retain_days,
    #     interactive = args.interactive,
    #     dry_run = args.dry_run,
    #     delete_batch_size = args.delete_batch_size,
    #     delete_quietly = args.delete_quietly,
    #     log_level = args.log_level,
    # )

    print(vars(args))
