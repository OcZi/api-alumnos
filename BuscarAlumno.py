import boto3
import json


def load_body(event):
    if 'body' not in event:
        return event

    if isinstance(event["body"], dict):
        return event['body']
    else:
        return json.loads(event['body'])


def lambda_handler(event, context):
    body = load_body(event)
    tenant_id = body.get('tenant_id')
    alumno_id = body.get('alumno_id')

    if not tenant_id or not alumno_id:
        return {
            'statusCode': 400,
            'body': json.dumps("Faltan parámetros")
        }

    table = boto3.resource('dynamodb').Table('t_alumnos')
    response = table.get_item(
        Key={
            'tenant_id': tenant_id,
            'alumno_id': alumno_id
        }
    )

    item = response.get('Item')
    if not item:
        return {
            'statusCode': 404,
            'body': json.dumps("Producto no encontrado")
        }

    return {
        'statusCode': 200,
        'body': json.dumps(item)
    }
