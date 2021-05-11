'''
This code is a Python3 version of index.js.
There are several functions omitted and changed from index.js.
1. No impelemetation of backoff algorithm.
2. No use of dynamoDB.batchWrite(Substituted for table.put_item)

You can surely save your data to DynamoDB without above functions.
However, it cannot handle errors stemmed from the duration of saving and getting data.
'''


from decimal import Decimal
from chalice import Chalice
import base64
import boto3
import json

app = Chalice(app_name='WildRydesStreamProcessor')
app.debug = True

@app.on_kinesis_record(stream='wildrydes-summary')
def WildRydesStreamProcessor_python(event):
    table = boto3.resource('dynamodb').Table('UnicornSensorData')
    
    for record in event:
        # The .data attribute is automatically base64 decoded for you.
        # DynamoDB only accepts Decimal type so change float to Decimal
        data = json.loads(record.data,parse_float=Decimal)
        app.log.debug("Received message with contents: %s", data)
        table.put_item(Item=data)
        
        

    
    
