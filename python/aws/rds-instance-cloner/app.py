#!/usr/bin/env python3.12

import boto3
import logging
import os

from datetime import date
from time import sleep

LOG_LEVEL = os.environ.get("LOG_LEVEL", logging.INFO)
logging.basicConfig(
    level  = LOG_LEVEL,
    format = "%(asctime)s :: %(name)s.%(funcName)s :: %(levelname)-8s :: %(message)s",
)

DRY_RUN = os.environ.get("DRY_RUN", str(True)).lower() in ["1", "true", "yes"]
SOURCE_DB_INSTANCE_IDENTIFIER: str = os.environ.get("SOURCE_DB_INSTANCE_IDENTIFIER")
CLONE_DB_INSTANCE_IDENTIFIER: str = os.environ.get("CLONE_DB_INSTANCE_IDENTIFIER", f"{SOURCE_DB_INSTANCE_IDENTIFIER}-clone-{date.today()}")
CLONE_MASTER_USER_PASSWORD: str = os.environ.get("CLONE_MASTER_USER_PASSWORD")
CLONE_METHOD: str = os.environ.get("CLONE_METHOD", "auto")

logger = logging.getLogger()
logger.debug(vars())

rds = boto3.client("rds")

def _change_rds_db_instance_master_user_password(
        db_instance_identifier: str,
        master_user_password: str,
        log_level: str = LOG_LEVEL,
) -> any:
    """
    Change the master user password of an existing RDS instance immediately.

    Calls RDS' ModifyDBInstance API.<br/>
    Refer <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/client/modify_db_instance.html>
    and <https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_ModifyDBInstance.html>.
    """

    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    response = rds.modify_db_instance(
        DBInstanceIdentifier = db_instance_identifier,
        MasterUserPassword   = master_user_password,
        ApplyImmediately     = True,
    )
    logger.debug("Response: %s", response)

    return response

def _describe_rds_db_instance(
        db_instance_identifier: str,
        log_level: str = LOG_LEVEL,
) -> any:
    """
    Describe an existing RDS instance.

    Calls RDS' DescribeDBInstances API.<br/>
    Refer <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/client/describe_db_instances.html>
    and <https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_DescribeDBInstances.html>.
    """

    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    response = rds.describe_db_instances(
        DBInstanceIdentifier = db_instance_identifier,
    )
    logger.debug("Response: %s", response)

    assert len(response["DBInstances"]) == 1, "Got more than the expected single RDS DB instance"
    return response["DBInstances"][0]

def _describe_rds_db_snapshots_for_instance(
        db_instance_identifier: str,
        log_level: str = LOG_LEVEL,
) -> any:
    """
    Describe existing RDS DB snapshots for a DB instance.

    Calls RDS' DescribeDBSnapshots API.<br/>
    Refer <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/client/describe_db_snapshots.html>
    and <https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_DescribeDBSnapshots.html>.
    """

    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    response = rds.describe_db_snapshots(
        DBInstanceIdentifier = db_instance_identifier,
    )
    logger.debug("Response: %s", response)

    return response

def _restore_rds_db_instance_from_snapshot(
        db_instance_identifier: str,
        db_snapshot_identifier: str,
        log_level: str = LOG_LEVEL,
        dry_run: bool = DRY_RUN,
) -> any:
    """
    Restore an RDS DB instance from snapshot.

    Calls RDS' RestoreDBInstanceFromDBSnapshot API.<br/>
    Refer <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/client/restore_db_instance_from_db_snapshot.html>
    and <https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_RestoreDBInstanceFromDBSnapshot.html>.
    """

    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    response = {}
    if dry_run is True:
        logger.info("Faking restoring RDS DB snapshot %s as DB instance %s", db_snapshot_identifier, db_instance_identifier)
        response["DBInstanceIdentifier"] = db_instance_identifier
        response["DBInstanceStatus"] = "available"
    else:
        logger.info("Restoring RDS DB snapshot %s as DB instance %s", db_snapshot_identifier, db_instance_identifier)
        response = rds.restore_db_instance_from_db_snapshot(
            DBInstanceIdentifier = db_instance_identifier,
            DBSnapshotIdentifier = db_snapshot_identifier,
        )
        logger.debug("Response: %s", response)
        _wait_for_rds_db_instance_to_be_in_status_available(db_instance_identifier)

    return response

def _restore_rds_db_instance_to_point_in_time_restore(
    source_db_instance_identifier: str,
    target_db_instance_identifier: str,
    restore_time: str | None = None,
    use_latest_restorable_time: bool = False,
    log_level: str = LOG_LEVEL,
    dry_run: bool = DRY_RUN,
):
    """
    Restore RDS from point-in-time.

    Calls RDS' RestoreDBInstanceToPointInTime API.<br/>
    Refer <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/client/restore_db_instance_to_point_in_time.html>
    and <https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_RestoreDBInstanceToPointInTime.html>.
    """

    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    response = {}
    if dry_run is True:
        logger.info("Faking restoring RDS DB instance %s to point in time as %s", source_db_instance_identifier, target_db_instance_identifier)
        response["DBInstanceStatus"] = "available"
    else:
        logger.info("Restoring RDS DB instance %s to point in time as %s", source_db_instance_identifier, target_db_instance_identifier)
        args = {
            "SourceDBInstanceIdentifier": source_db_instance_identifier,
            "TargetDBInstanceIdentifier": target_db_instance_identifier,
        }
        # these are mutually exclusive
        if use_latest_restorable_time is False:
            args["RestoreTime"] = restore_time
        else:
            args["UseLatestRestorableTime"] = use_latest_restorable_time
        response = rds.restore_db_instance_to_point_in_time(**args)
        logger.debug("Response: %s", response)
        _wait_for_rds_db_instance_to_be_in_status_available(target_db_instance_identifier)

    return response

def _wait_for_rds_db_instance_to_be_in_status_available(
    db_instance_identifier: str,
    delay: int = 30,
    max_attempts: int = 120,
    log_level: str = LOG_LEVEL,
):
    """
    Wait for an existing RDS instance to be available.

    Refer <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/client/describe_db_instances.html>.
    """

    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    waiter = rds.get_waiter("db_instance_available")
    waiter.wait(
        DBInstanceIdentifier = db_instance_identifier,
        WaiterConfig={
            'Delay': delay,
            'MaxAttempts': max_attempts
        }
    )

def clone_rds_db_instance(
    source_db_instance_identifier: str,
    clone_db_instance_identifier: str,
    method: str = CLONE_METHOD,
    log_level: str = LOG_LEVEL,
) -> any:
    """
    Clone an existing RDS instance.
    """

    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    if method.lower() in ["auto"]:
        rds_db_instance = _describe_rds_db_instance(source_db_instance_identifier)
        if rds_db_instance["BackupRetentionPeriod"] > 0:
            method = "pitr"
        else:
            method = "snapshot"

    if method.lower() in ["pitr"]:
        logger.info("Cloning RDS DB instance via Point-in-Time Restore (PITR)")
        _restore_rds_db_instance_to_point_in_time_restore(
            source_db_instance_identifier = source_db_instance_identifier,
            target_db_instance_identifier = clone_db_instance_identifier,
            use_latest_restorable_time    = True,
        )
    else:
        logger.info("Getting the RDS DB instance's snapshots")
        snapshots = _describe_rds_db_snapshots_for_instance(
            db_instance_identifier = source_db_instance_identifier,
        )
        logger.info("Cloning RDS DB instance using its latest snapshot")
        _restore_rds_db_instance_from_snapshot(
            db_instance_identifier = clone_db_instance_identifier,
            db_snapshot_identifier = "",  # FIXME
        )


if __name__ == "__main__":
    assert SOURCE_DB_INSTANCE_IDENTIFIER not in [None, ""], "SOURCE_DB_INSTANCE_IDENTIFIER cannot be None nor the empty string"
    assert CLONE_DB_INSTANCE_IDENTIFIER  not in [None, ""], "CLONE_DB_INSTANCE_IDENTIFIER cannot be None nor the empty string"
    clone_rds_db_instance(
        source_db_instance_identifier = SOURCE_DB_INSTANCE_IDENTIFIER,
        clone_db_instance_identifier  = CLONE_DB_INSTANCE_IDENTIFIER,
    )
    if CLONE_MASTER_USER_PASSWORD not in [None, ""]:
        _change_rds_db_instance_master_user_password(
            db_instance_identifier = CLONE_DB_INSTANCE_IDENTIFIER,
            master_user_password   = CLONE_MASTER_USER_PASSWORD,
        )
