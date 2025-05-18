from services.usuarios.usuarios import (
    listar_usuarios,
    inserir_usuario,
    excluir_usuario,
    atualizar_usuario,
)
from services.auditoria_usuarios.auditoria import processar_auditoria
from services.usuarios.usuarios_topico import consumir_usuario_teste


def listarUsuarios(event, context):
    return listar_usuarios(event, context)


def inserirUsuarios(event, context):
    return inserir_usuario(event, context)


def excluirUsuarios(event, context):
    return excluir_usuario(event, context)


def atualizarUsuarios(event, context):
    return atualizar_usuario(event, context)


def auditoriaProcessa(event, context):
    return processar_auditoria(event, context)


def consumirUsuarioTeste(event, context):
    return consumir_usuario_teste(event, context)
