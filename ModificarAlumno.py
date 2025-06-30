import boto3


def load_body(event):
    if 'body' not in event:
        return event

    if isinstance(event["body"], dict):
        return event['body']
    else:
        return json.loads(event['body'])


def lambda_handler(event, context):
    # Entrada (json)
    body = load_body(event)
    tenant_id = body['tenant_id']
    alumno_id = body['alumno_id']
    updates = body.get("updates", {})

    if not tenant_id or not alumno_id or not updates:
        return {
            'statusCode': 400,
            'body': json.dumps("Faltan parámetros: tenant_id o alumno_id")
        }
    
    table = boto3.resource('dynamodb').Table('t_alumnos')

    update_expr = "SET " + ", ".join(f"{k}= :{k}" for k in updates)
    expr_values = {f":{k}": v for k, v in updates.items()}

    table.update_item(
        Key={'tenant_id': tenant_id, 'alumno_id': alumno_id},
        UpdateExpression=update_expr,
        ExpressionAttributeValues=expr_values)
   return {'statusCode': 200, 'body': json.dumps("Alumno modificado")}