import boto3
import json

def lambda_handler(event, context):
    body = json.loads(event['body'])
    tenant_id = body.get('tenant_id')
    producto_id = body.get('producto_id')

    if not tenant_id or not producto_id:
        return {
            'statusCode': 400,
            'body': json.dumps("Faltan parámetros")
        }

    table = boto3.resource('dynamodb').Table('t_productos')
    response = table.get_item(
        Key={
            'tenant_id': tenant_id,
            'producto_id': producto_id
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
