from decimal import Decimal
from chalice import Chalice
import base64
import boto3
import json

app = Chalice(app_name='WildRydesStreamProcessor')
app.debug = True


#def lambda_handler(event, context):
#   buildRequestItems(event['Records'])
    

@app.on_kinesis_record(stream='wildrydes')
def buildRequestItems(event):
    table = boto3.resource('dynamodb').Table('UnicornSensorData')
    
    for record in event:
        # The .data attribute is automatically base64 decoded for you.
        # DynamoDB only accepts Decimal type so change float to Decimal
        data = json.loads(record.data,parse_float=Decimal)
        app.log.debug("Received message with contents: %s", data)
        table.put_item(Item=data)
        
        

    
    
