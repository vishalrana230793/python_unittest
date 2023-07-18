import os
from router.Router import Router
if os.getenv('ENV', default='LOCAL') == 'LOCAL':
    from dotenv import load_dotenv
    load_dotenv()

def lambda_handler(event, context):
    return Router.router(event=event)


if __name__ == '__main__':
    import json
    print(lambda_handler(event=json.load(open(r'check_event.json', 'r')), context=None))