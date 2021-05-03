from chalice import Chalice
import base64
import json

app = Chalice(app_name='WildRydesStreamProcessor')
app.debug = True


#def lambda_handler(event, context):
#   buildRequestItems(event['Records'])
    

@app.on_kinesis_record(stream='wildrydes')
def buildRequestItems(event):
    for record in event:
        # The .data attribute is automatically base64 decoded for you.
        app.log.debug("Received message with contents: %s", record.data)
    
    
