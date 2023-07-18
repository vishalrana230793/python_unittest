import os
import sys
sys.path.append('./')
import json
import pytest
from unittest.mock import patch
from router.Router import Router
if os.getenv('ENV', default='LOCAL') == 'LOCAL':
    from dotenv import load_dotenv
    load_dotenv()

class TestServiceHandler:
    @pytest.fixture(scope="session")
    def event_valid(request):
        return {'resource':'/check'}
    
    @pytest.fixture(scope="session")
    def event_invalid(request):
        return {'resource':'/none'}
        
    def test_router_successful(self, event_valid):
        with patch('app.App.App.check') as mock_app_call:
            mock_app_call.return_value = 'Hello'
            assert Router.router(event_valid)
    
    def test_router_unsuccessful(self, event_invalid):
        result = Router.router(event_invalid)
        assert result['statusCode'] == 400