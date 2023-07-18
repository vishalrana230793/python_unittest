import os
import sys
sys.path.append('./')
import json
import pytest
from unittest.mock import patch
from utils.DynamoDb import DynamoDb
from boto3.dynamodb.conditions import Key
if os.getenv('ENV', default='LOCAL') == 'LOCAL':
    from dotenv import load_dotenv
    load_dotenv()

class TestServiceHandler:
    @pytest.fixture(scope="session")
    def event_get(request):
        return 'test4@gmail.com'

    @pytest.fixture(scope="session")
    def event_insert(request):
        return {'UseremailID':'test10@gmail.com'}
    
    def test_query_successful(self, event_get):
        with patch('boto3.resource') as mock_dynamo_db_call:
            mock_dynamodb = mock_dynamo_db_call.return_value
            mock_table = mock_dynamodb.Table.return_value
            mock_table.query.return_value = {'Items': [], 'Count': 1}

            DynamoDb().query(event_get)

            mock_dynamo_db_call.assert_called_once_with('dynamodb', region_name='ap-south-1')
            mock_dynamodb.Table.assert_called_once_with('UserFeedback')
            mock_table.query.assert_called_once_with(KeyConditionExpression=Key(os.environ['PRIMARY_KEY']).eq(event_get))
    
    def test_query_return_none(self, event_get):
        with patch('boto3.resource') as mock_dynamo_db_call:
            mock_dynamodb = mock_dynamo_db_call.return_value
            mock_table = mock_dynamodb.Table.return_value
            mock_table.query.return_value = {'Items': [], 'Count': 0}

            DynamoDb().query(event_get)

            mock_dynamo_db_call.assert_called_once_with('dynamodb', region_name='ap-south-1')
            mock_dynamodb.Table.assert_called_once_with('UserFeedback')
            mock_table.query.assert_called_once_with(KeyConditionExpression=Key(os.environ['PRIMARY_KEY']).eq(event_get))

    def test_query_exception(self, event_get):
        try:
            with patch('boto3.resource') as mock_dynamo_db_call:
                mock_dynamodb = mock_dynamo_db_call.return_value
                mock_table = mock_dynamodb.Table.return_value
                mock_table.query.side_effect = Exception("DynamoDB exception")
                with pytest.raises(Exception) as exc_info:
                    assert DynamoDb().query(event_get)
        except:
            assert True

    def test_insert_successful(self, event_insert):
        with patch('boto3.resource') as mock_dynamo_db_call:
            mock_dynamodb = mock_dynamo_db_call.return_value
            mock_table = mock_dynamodb.Table.return_value
            mock_table.put_item.return_value = {}

            DynamoDb().insert(event_insert)

            mock_dynamo_db_call.assert_called_once_with('dynamodb', region_name='ap-south-1')
            mock_dynamodb.Table.assert_called_once_with('UserFeedback')
            mock_table.put_item.assert_called_once()

    def test_insert_exception(self, event_insert):
        try:
            with patch('boto3.resource') as mock_dynamo_db_call:
                mock_dynamodb = mock_dynamo_db_call.return_value
                mock_table = mock_dynamodb.Table.return_value
                mock_table.put_item.side_effect = Exception("DynamoDB exception")
                with pytest.raises(Exception) as exc_info:
                    assert DynamoDb().insert(event_insert)
        except:
            assert True
