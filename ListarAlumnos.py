import boto3  # import Boto3
from boto3.dynamodb.conditions import Key  # import Boto3 conditions


def load_body(event):
    if 'body' not in event:
        return event

    if isinstance(event["body"], dict):
        return event['body']
    else:
        return json.loads(event['body'])


def lambda_handler(event, context):
    # Entrada (json)
    print(event)
    body = load_body(event["body"])
    tenant_id = body['tenant_id']
    # Proceso
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')
    response = table.query(
        KeyConditionExpression=Key('tenant_id').eq(tenant_id)
    )
    items = response['Items']
    num_reg = response['Count']
    print(items)
    # Salida (json)
    return {
        'statusCode': 200,
        'tenant_id':tenant_id,
        'num_reg': num_reg,
        'alumnos': items
    }
