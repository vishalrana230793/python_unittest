import json
from app.App import App
import os

class Router:
    @staticmethod
    def router(event):
        if event['resource'] == os.environ['CHECK_FEEDBACK_PATH']:
            return App.check(event=event)
        else:
            return { 
                'statusCode': 400, 
                'headers': { 
                    'Access-Control-Allow-Origin': '*', 
                    'Access-Control-Allow-Credentials': 'true' 
                }, 
                'body':json.dumps({ 
                    'status':False, 
                    'message':'Invalid Resource Path!'
                    }
                )
            }