import json
import os
import boto3

API_KEY = os.environ.get('API_KEY')
METRIC_NAMESPACE = os.environ.get('METRIC_NAMESPACE', 'HotWater')

cw = boto3.client('cloudwatch')

def lambda_handler(event, context):
    headers = event.get('headers') or {}
    # Normalize header keys to lowercase
    headers = {k.lower(): v for k, v in headers.items()}

    if headers.get('x-api-key') != API_KEY:
        return {
            'statusCode': 401,
            'body': json.dumps({'message': 'Unauthorized'})
        }

    body = event.get('body')
    if not body:
        return {'statusCode': 400, 'body': json.dumps({'message': 'Empty body'})}

    if event.get('isBase64Encoded'):
        import base64
        body = base64.b64decode(body).decode('utf-8')

    try:
        data = json.loads(body)
        device = data['device']
        temperature = float(data['temperature_c'])
    except Exception as e:
        return {'statusCode': 400, 'body': json.dumps({'message': 'Bad request', 'error': str(e)})}

    # Push custom metric
    try:
        cw.put_metric_data(
            Namespace=METRIC_NAMESPACE,
            MetricData=[
                {
                    'MetricName': 'TemperatureC',
                    'Dimensions': [
                        {'Name': 'Device', 'Value': device}
                    ],
                    'Value': temperature
                }
            ]
        )
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'message': 'Failed to put metric', 'error': str(e)})}

    return {
        'statusCode': 200,
        'body': json.dumps({'status': 'ok'})
    }
