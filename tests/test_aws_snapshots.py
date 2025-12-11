import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone, timedelta
from ops_core.aws.snapshots import cleanup_snapshots


class TestSnapshotCleaner(unittest.TestCase):

    def setUp(self):
        """Configuracion base para cada test."""
        self.mock_config = {
            "aws": {
                "snapshots": {
                    "retention_days": 10,
                    "dry_run": False,
                    "regions": ["us-east-1"],
                    "allowed_account_ids": ["123456789"],
                }
            }
        }

    @patch("ops_core.aws.snapshots.boto3.client")
    @patch(
        "ops_core.aws.snapshots.verify_account"
    )  # Bypasseamos el check de seguridad real
    def test_cleanup_deletes_old_snapshots(self, mock_verify, mock_boto_client):
        """Prueba que los snapshots viejos se eliminan y los nuevos se conservan."""

        # 1. Configurar el Mock de EC2
        mock_ec2 = MagicMock()
        mock_boto_client.return_value = mock_ec2

        # 2. Definir fechas
        now = datetime.now(timezone.utc)
        old_date = now - timedelta(days=20)  # Deberia borrarse (Retention=10)
        new_date = now - timedelta(days=2)  # Deberia conservarse

        # 3. Simular respuesta de AWS (describe_snapshots)
        mock_ec2.describe_snapshots.return_value = {
            "Snapshots": [
                {"SnapshotId": "snap-old", "StartTime": old_date},
                {"SnapshotId": "snap-new", "StartTime": new_date},
            ]
        }

        # 4. Ejecutar la funcion
        cleanup_snapshots(self.mock_config)

        # 5. Aserciones (Verificaciones)

        # Verificar que se llamo a describe_snapshots
        mock_ec2.describe_snapshots.assert_called_with(OwnerIds=["self"])

        # Verificar que delete_snapshot se llamo SOLO para el viejo
        mock_ec2.delete_snapshot.assert_called_once_with(SnapshotId="snap-old")

    @patch("ops_core.aws.snapshots.boto3.client")
    @patch("ops_core.aws.snapshots.verify_account")
    def test_dry_run_does_not_delete(self, mock_verify, mock_boto_client):
        """Prueba que con dry_run=True NO se llama a borrar."""

        # Forzar Dry Run
        self.mock_config["aws"]["snapshots"]["dry_run"] = True

        mock_ec2 = MagicMock()
        mock_boto_client.return_value = mock_ec2

        old_date = datetime.now(timezone.utc) - timedelta(days=20)
        mock_ec2.describe_snapshots.return_value = {
            "Snapshots": [{"SnapshotId": "snap-old", "StartTime": old_date}]
        }

        cleanup_snapshots(self.mock_config)

        # Verificar que delete_snapshot NUNCA se llamo
        mock_ec2.delete_snapshot.assert_not_called()
