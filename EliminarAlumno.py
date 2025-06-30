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
    tenant_id = body["tenant_id"]
    alumno_id = body["alumno_id"]

    if not tenant_id or not alumno_id:
        return {
            'statusCode': 400,
            'body': json.dumps("Faltan parámetros: tenant_id o alumno_id")
        }
    
    tenant_id = body['tenant_id']
    alumno_id = body['alumno_id']

    table = boto3.resource('dynamodb').Table('t_alumnos')
    response = table.delete_item(Key={
        'tenant_id': tenant_id,
        'alumno_id': alumno_id
    })
    # Salida (json)
    return {
        'statusCode': 200,
        'response': response
    }
