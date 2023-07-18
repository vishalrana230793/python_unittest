import json
from utils.DynamoDb import DynamoDb

class App:
    @staticmethod
    def check(event):
        UseremailID = event['queryStringParameters']['UseremailID']
        res, error = DynamoDb().query(UseremailID=UseremailID)
        # print(res)
        if error is None and res is not False:
            return { 
                    'statusCode': 200, 
                    'headers': { 
                        'Access-Control-Allow-Origin': '*', 
                        'Access-Control-Allow-Credentials': 'true' 
                    }, 
                    'body':json.dumps({ 
                        'status':True, 
                        'message':'Data Fetched!',
                        'data':json.loads(res)
                        }
                    )
            }
        elif error is None and res is False:
            return { 
                    'statusCode': 404, 
                    'headers': { 
                        'Access-Control-Allow-Origin': '*', 
                        'Access-Control-Allow-Credentials': 'true' 
                    }, 
                    'body':json.dumps({ 
                        'status':False, 
                        'message':'No Data Found!',
                        'data':{}
                        }
                    )
            }
        else:
            return { 
                    'statusCode': 500, 
                    'headers': { 
                        'Access-Control-Allow-Origin': '*', 
                        'Access-Control-Allow-Credentials': 'true' 
                    }, 
                    'body':json.dumps({ 
                        'status':False, 
                        'error':error
                    }
                )
            }