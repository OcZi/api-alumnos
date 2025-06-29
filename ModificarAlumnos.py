import boto3
import json

def lambda_handler(event, context):
    body = json.loads(event['body'])
    tenant_id = body.get('tenant_id')
    producto_id = body.get('producto_id')
    updates = body.get('updates')

    if not tenant_id or not producto_id or not updates:
        return {
            'statusCode': 400,
            'body': json.dumps("Faltan parámetros")
        }

    update_expr = "SET " + ", ".join(f"{k}= :{k}" for k in updates.keys())
    expr_values = {f":{k}": v for k, v in updates.items()}

    table = boto3.resource('dynamodb').Table('t_productos')
    table.update_item(
        Key={'tenant_id': tenant_id, 'producto_id': producto_id},
        UpdateExpression=update_expr,
        ExpressionAttributeValues=expr_values
    )

    return {
        'statusCode': 200,
        'body': json.dumps("Producto modificado")
    }
