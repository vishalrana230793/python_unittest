import boto3
from boto3.dynamodb.conditions import Key
import os
import json
import decimal

class DynamoDb:
    def __init__(self):
        self.__DYNAMODB = boto3.resource('dynamodb', region_name=os.environ['DYNAMO_DB_REGION'])

    def insert(self, data:dict):
        try:
            table = self.__DYNAMODB.Table(os.environ['DYNAMO_DB_TABLE_NAME'])
            table.put_item(Item=data)
            return True, None
        except Exception as ex:
            return False, str(ex)

    def query(self, UseremailID:str):
        try:
            table = self.__DYNAMODB.Table(os.environ['DYNAMO_DB_TABLE_NAME'])
            response = table.query(
                KeyConditionExpression = Key(os.environ['PRIMARY_KEY']).eq(UseremailID)
            )
            if response['Count'] > 0:
                return json.dumps((response['Items']), indent=4, cls=DecimalEncoder), None
            else:
                return False, None
        except Exception as ex:
            return False, str(ex)

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        if isinstance(o, set):
            return list(o)
        return super(DecimalEncoder, self).default(o)
    
# if __name__ == '__main__':
#     import pytz
#     from dotenv import load_dotenv
#     load_dotenv()
#     DynamoDb().insert(data={
#         'Username':'test 2',
#         'UseremailID':'test3@msil.co.in',
#         'Company':'test org 2',
#         'Performace':3,
#         'Clarity':4,
#         'LastModifiedStamp': str(datetime.now(tz=pytz.timezone('Asia/Kolkata')).date())
#     })

    # print(DynamoDb().query(UseremailID='test4@msil.co.in'))