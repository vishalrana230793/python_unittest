import os
import sys
sys.path.append('./')
import json
import pytest
from unittest.mock import patch
from app.App import App
if os.getenv('ENV', default='LOCAL') == 'LOCAL':
    from dotenv import load_dotenv
    load_dotenv()

class TestServiceHandler:
    @pytest.fixture(scope="session")
    def event_200_email_id(request):
        return {
            'queryStringParameters':{
                'UseremailID':'test4@gmail.com'
            }
        }

    @pytest.fixture(scope="session")
    def event_404_email_id(request):
        return {
            'queryStringParameters':{
                'UseremailID':'test10@gmail.com'
            }
        }

    @pytest.fixture(scope="session")
    def event_500_email_id(request):
        return {
            'queryStringParameters':{
                'UseremailID':'test500@gmail.com'
            }
        }
    
    def test_app_for_200(self, event_200_email_id):
        with patch('utils.DynamoDb.DynamoDb.query') as mock_dynamo_db_call:
            mock_dynamo_db_call.return_value = [json.dumps([{}]), None]
            result = App.check(event_200_email_id)
        assert result['statusCode'] == 200
    
    def test_app_for_404(self, event_404_email_id):
        with patch('utils.DynamoDb.DynamoDb.query') as mock_dynamo_db_call:
            mock_dynamo_db_call.return_value = [False, None]
            result = App.check(event_404_email_id)
        assert result['statusCode'] == 404
    
    def test_app_for_500(self, event_500_email_id):
        with patch('utils.DynamoDb.DynamoDb.query') as mock_dynamo_db_call:
            mock_dynamo_db_call.return_value = [False, 500]
            result = App.check(event_500_email_id)
        assert result['statusCode'] == 500