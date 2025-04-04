# filepath: /Users/piyush/Copilot/RDS-Downgrade/test_Lambda-RDSdowngrade.py
import unittest
from unittest.mock import patch, MagicMock
from Lambda_RDSdowngrade import lambda_handler, is_cpu_utilization_low, is_within_maintenance_window, downgrade_instance

class TestLambdaRDSDowngrade(unittest.TestCase):
    @patch('Lambda-RDSdowngrade.rds_client')
    @patch('Lambda-RDSdowngrade.cloudwatch_client')
    def test_lambda_handler(self, mock_cloudwatch, mock_rds):
        # Mock RDS describe_db_instances response
        mock_rds.describe_db_instances.return_value = {
            'DBInstances': [
                {'DBInstanceIdentifier': 'test-instance', 'DBInstanceClass': 'db.t3.medium'}
            ]
        }

        # Mock CPU utilization check
        with patch('Lambda-RDSdowngrade.is_cpu_utilization_low', return_value=True):
            # Mock maintenance window check
            with patch('Lambda-RDSdowngrade.is_within_maintenance_window', return_value=True):
                # Mock downgrade instance
                with patch('Lambda-RDSdowngrade.downgrade_instance') as mock_downgrade:
                    lambda_handler({}, {})
                    mock_downgrade.assert_called_once_with('test-instance')

if __name__ == '__main__':
    unittest.main()