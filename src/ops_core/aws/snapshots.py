import boto3
from datetime import datetime, timezone, timedelta
from botocore.exceptions import ClientError
from ops_core.common.log import get_logger

logger = get_logger(__name__)


def verify_account(allowed_ids: list):
    """
    Verifica que el script se esté ejecutando en una cuenta permitida.
    Lanza una excepción si la cuenta actual no está en la lista blanca.
    """
    if not allowed_ids:
        logger.warning(
            "No allowed_account_ids defined in config. Skipping safety check."
        )
        return

    sts = boto3.client("sts")
    current_account = sts.get_caller_identity()["Account"]

    if current_account not in allowed_ids:
        error_msg = (
            f"SAFETY STOP: Current AWS Account ({current_account}) "
            f"is NOT in the allowed list {allowed_ids}. Aborting."
        )
        logger.critical(error_msg)
        raise PermissionError(error_msg)

    logger.info(f"Identity verified: Running on account {current_account}")


def cleanup_snapshots(config: dict):
    aws_config = config.get("aws", {}).get("snapshots", {})

    # 1. Configurar variables
    retention_days = aws_config.get("retention_days", 30)
    dry_run = aws_config.get("dry_run", True)
    regions = aws_config.get("regions", ["us-east-1"])
    allowed_ids = aws_config.get("allowed_account_ids", [])

    # 2. Verificar Cuenta (Safety Catch)
    # Convertimos los IDs a string por seguridad
    allowed_ids = [str(aid) for aid in allowed_ids]
    verify_account(allowed_ids)

    logger.info(
        f"Starting AWS Snapshot Cleanup. Retention: {retention_days} days. "
        f"Dry Run: {dry_run}"
    )

    cutoff_date = datetime.now(timezone.utc) - timedelta(days=retention_days)

    for region in regions:
        logger.info(f"Checking region: {region}")
        try:
            ec2 = boto3.client("ec2", region_name=region)

            # Obtener snapshots SOLO del propietario
            response = ec2.describe_snapshots(OwnerIds=["self"])
            snapshots = response["Snapshots"]

            logger.info(f"Found {len(snapshots)} snapshots in {region}")

            for snap in snapshots:
                snap_id = snap["SnapshotId"]
                snap_date = snap["StartTime"]

                if snap_date < cutoff_date:
                    if dry_run:
                        logger.info(
                            f"[DRY RUN] Would delete snapshot {snap_id} "
                            f"created on {snap_date}"
                        )
                    else:
                        try:
                            ec2.delete_snapshot(SnapshotId=snap_id)
                            logger.info(
                                f"Deleted snapshot {snap_id} created on {snap_date}"
                            )
                        except ClientError as e:
                            if "InvalidSnapshot.InUse" in str(e):
                                logger.warning(
                                    f"Skipping {snap_id}: Snapshot is in use."
                                )
                            else:
                                logger.error(f"Failed to delete {snap_id}: {e}")
                else:
                    logger.debug(
                        f"Snapshot {snap_id} is recent ({snap_date}). Keeping."
                    )

        except Exception as e:
            logger.error(f"Error processing region {region}: {e}")
