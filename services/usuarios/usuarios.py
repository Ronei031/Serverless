import json
import boto3 # type: ignore
import uuid
from utils.response import response
from services.auditoria_usuarios.auditoria import publicar_auditoria
from services.usuarios.usuarios_topico import publicar_usuario_criado


dynamodb = boto3.resource("dynamodb")
tabela_usuarios = dynamodb.Table("Usuarios")
sns = boto3.client("sns")


def listar_usuarios(event, context):
    try:
        result = tabela_usuarios.scan()
        return response(200, result.get("Items", []))
    except Exception as e:
        print(f"Erro ao listar usuários: {e}")
        return response(500, {"error": str(e)})


def inserir_usuario(event, context):
    try:
        data = json.loads(event["body"])
        nome = data.get("nome")
        email = data.get("email")

        if (
            not nome
            or not isinstance(nome, str)
            or not email
            or not isinstance(email, str)
        ):
            return response(
                400,
                {
                    "error": "Os campos 'nome' e 'email' são obrigatórios e devem ser strings"
                },
            )

        usuario_id = str(uuid.uuid4())

        item = {"id": usuario_id, "nome": nome, "email": email}
        tabela_usuarios.put_item(Item=item)

        publicar_auditoria("inserir", item)
        publicar_usuario_criado(item)

        return response(
            201, {"message": "Usuário inserido com sucesso!", "id": usuario_id}
        )
    except Exception as e:
        print(f"Erro ao inserir usuário: {e}")
        return response(500, {"error": str(e)})


def atualizar_usuario(event, context):
    try:
        usuario_id = event.get("pathParameters", {}).get("id")
        if not usuario_id:
            return response(400, {"error": "ID do usuário não fornecido"})

        data = json.loads(event["body"])
        nome = data.get("nome")
        email = data.get("email")

        if (
            not nome
            or not isinstance(nome, str)
            or not email
            or not isinstance(email, str)
        ):
            return response(
                400,
                {
                    "error": "Os campos 'nome' e 'email' são obrigatórios e devem ser strings"
                },
            )

        result = tabela_usuarios.update_item(
            Key={"id": usuario_id},
            UpdateExpression="set nome=:n, email=:e",
            ExpressionAttributeValues={":n": nome, ":e": email},
            ReturnValues="ALL_NEW",
        )

        publicar_auditoria("atualizar", result["Attributes"])

        return response(
            200,
            {
                "message": "Usuário atualizado com sucesso!",
                "usuario": result["Attributes"],
            },
        )
    except Exception as e:
        print(f"Erro ao atualizar usuário: {e}")
        return response(500, {"error": str(e)})


def excluir_usuario(event, context):
    try:
        usuario_id = event.get("pathParameters", {}).get("id")
        if not usuario_id:
            return response(400, {"error": "ID do usuário não fornecido"})

        resp = tabela_usuarios.delete_item(
            Key={"id": usuario_id}, ReturnValues="ALL_OLD"
        )

        if "Attributes" in resp:
            publicar_auditoria("excluir", resp["Attributes"])
            return response(200, {"message": "Usuário excluído com sucesso!"})

        return response(404, {"error": "Usuário não encontrado"})
    except Exception as e:
        print(f"Erro ao excluir usuário: {e}")
        return response(500, {"error": str(e)})
