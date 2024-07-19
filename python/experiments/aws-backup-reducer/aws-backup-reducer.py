#!/usr/bin/env python3.12

import boto3
import logging

from datetime import datetime, timedelta, UTC
from itertools import batched, groupby

def delete_old_backups(
    bucket: str,
    prefix: str = '',
    days_to_retain_all_objects: int = 30,
    interactive: bool = True,
    batch_size: int = 1000,
    dry_run: bool = True,
    delete_quietly: bool = False,
):

    """
    Delete old backups

    Retain days_to_retain_all_objects days worth of objects, then 1 per week for 1 year, then 1 per year

    FIXME: check the bucket is not a _directory bucket_
    """

    assert bucket != '', 'bucket cannot be an empty string'
    assert batch_size >=1 and batch_size <= 1000, 'batch_size must be between 1 and 1000'

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.debug(vars())

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
        PaginationConfig = {
            'MaxItems': batch_size,
        },
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

    # lock the list of objects down
    # I do know my chickens
    objects = tuple(objects)

    # filter out objects last modified in the last x days to keep
    # filtering from the iterator using iterator.search and a jmespath query would have been the easiest option
    # … but yeah, jmespath queries, thanks but nah thanks
    actionable_objects = [obj for obj in objects if obj['LastModified'] < actionable_limit_date]
    logger.info(f'found {len(actionable_objects)} actionable objects')
    logger.debug(f'actionable objects {actionable_objects}')

    # filter out 1 object per year to keep
    # objects are ordered from the oldest to the most recent => grouping by year, the latest in each group set will be
    # the one to keep
    for k, v in groupby(actionable_objects, key = lambda obj: obj['LastModified'].isocalendar().year):
        objects_by_year = list(v)
        actionable_objects.remove(objects_by_year[-1])
        logger.info(f'filtered out object to keep for year {k}')
        logger.debug(f'filtered out object: {objects_by_year[-1]}')
    logger.debug(f'actionable objects reduced to {actionable_objects}')

    # filter out 1 object per week to keep
    # the requirement being 1y, no need to do this per year *and*, per week
    # grouping by week, the latest in each group set will be the one to keep
    for k, v in groupby(actionable_objects, key = lambda obj: obj['LastModified'].isocalendar().week):
        objects_by_week = list(v)
        actionable_objects.remove(objects_by_week[-1])
        logger.info(f'filtered out object to keep for week {k}')
        logger.debug(f'filtered out object: {objects_by_week[-1]}')
    logger.debug(f'actionable objects reduced to {actionable_objects}')

    # lock the list of actionable objects down
    # I do know my chickens
    actionable_objects = tuple(actionable_objects)

    # use one bulk request, it makes no sense to call it once per object
    # bulk requests can sustain up to 1000 objects at a time => send requests with batches
    for batch in batched(actionable_objects, batch_size):
        if interactive:
            print(f'About to {"faking" if dry_run else "really"} delete {len(batch)} objects.')
            proceed = input('Proceed?\n> ')
            if proceed.lower() not in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']:
                continue
            print(f'Batch skipped')
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
    delete_old_backups(bucket='backups', batch_size=5, dry_run=True)
