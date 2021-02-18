import json
import boto3


region = 'us-east-1'
s3_bucket = f"jumpstart-cache-prod-{region}"
key_prefix = "inference-notebook-assets"
s3 = boto3.client("s3")

def download_from_s3(key_filenames):
    for key_filename in key_filenames:
        s3.download_file(s3_bucket, f"{key_prefix}/{key_filename}", f"/tmp/{key_filename}")
    

def query_endpoint(img):
    endpoint_name = 'jumpstart-dft-tf-ic-imagenet-inception-v3-classificati'
    client = boto3.client('runtime.sagemaker')
    response = client.invoke_endpoint(EndpointName=endpoint_name, ContentType='application/x-image', Body=img)
    model_predictions = json.loads(response['Body'].read())['predictions'][0]
    return model_predictions


def lambda_handler(event, context):
    # TODO implement
    
    result = dict()
    cat_jpg, dog_jpg, ImageNetLabels = "cat.jpg", "dog.jpg", "ImageNetLabels.txt"
    download_from_s3(key_filenames=[cat_jpg, dog_jpg, ImageNetLabels])
    
    images = {}
    with open("/tmp/cat.jpg", 'rb') as file: images[cat_jpg] = file.read()
    with open("/tmp/dog.jpg", 'rb') as file: images[dog_jpg] = file.read()
    with open("/tmp/ImageNetLabels.txt", 'r') as file: class_id_to_label = file.read().splitlines()
    
    for filename, img in images.items():
        model_predictions = query_endpoint(img)  
        top5_prediction_ids = sorted(range(len(model_predictions)), key=lambda index: model_predictions[index], reverse=True)[:5]
        top5_class_labels = ", ".join([class_id_to_label[id] for id in top5_prediction_ids])
        result[filename] = top5_class_labels
        
        
    
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
    



