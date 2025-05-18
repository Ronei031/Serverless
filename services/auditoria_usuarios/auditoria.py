import json
import boto3 # type: ignore
import uuid
import os
from datetime import datetime

dynamodb = boto3.resource("dynamodb")
tabela_auditoria = dynamodb.Table("AuditoriaUsuarios")
sqs = boto3.client("sqs")
fila_url = os.environ.get("AUDITORIA_QUEUE_URL")


def processar_auditoria(event, context):
    try:
        for record in event["Records"]:
            mensagem = json.loads(record["body"])
            log_item = {
                "id": f"{mensagem['operacao']}_{uuid.uuid4()}",
                "operacao": mensagem["operacao"],
                "dados": mensagem["dados"],
                "timestamp": mensagem["timestamp"],
            }
            tabela_auditoria.put_item(Item=log_item)
    except Exception as e:
        print(f"Erro ao processar auditoria: {e}")
        raise e


def publicar_auditoria(operacao, dados):
    try:
        mensagem = {"operacao": operacao, "dados": dados, "timestamp": datetime.now().isoformat()}
        sqs.send_message(QueueUrl=fila_url, MessageBody=json.dumps(mensagem))
    except Exception as e:
        print(f"Erro ao publicar auditoria: {e}")
