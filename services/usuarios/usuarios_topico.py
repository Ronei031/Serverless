import os
import boto3 # type: ignore
import json

sns = boto3.client('sns')
dynamodb = boto3.resource('dynamodb')
tabela_teste = dynamodb.Table('UsuariosTeste')

SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_USUARIOS_CRIADOS_ARN')

def publicar_usuario_criado(usuario):
    if SNS_TOPIC_ARN:
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="Novo usuário criado",
            Message=json.dumps(usuario)
        )

def consumir_usuario_teste(event, context):
    try:
        for record in event['Records']:
            mensagem = record['Sns']['Message']
            usuario = json.loads(mensagem)

            # Salva o usuário na tabela de teste
            tabela_teste.put_item(Item=usuario)

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Usuários salvos na tabela de teste com sucesso!'})
        }
    except Exception as e:
        print(f"Erro ao processar mensagem SNS: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
