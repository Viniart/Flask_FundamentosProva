from datetime import datetime, timedelta
from . import app, db
from flask import request, make_response
from .models import Transacao
from sqlalchemy.sql import func

@app.route("/transacao", methods=["POST"])
def cadastrarTransacao():
    data = request.json
    valor = data.get("valor")
    dataHora = data.get("dataHora")

    if valor < 0:
        return make_response({}, 422)
    
    if datetime.fromisoformat(dataHora) > datetime.now():
        return make_response({}, 422)

    if valor and dataHora:
        transacao = Transacao(
            valor = valor,
            dataHora = dataHora
        )
        db.session.add(transacao)
        db.session.commit()
    return transacao.serialize

@app.route("/transacao", methods=["DELETE"])
def deletarTransacao():
    # Caso queira verificar tudo que foi deletador
    quantidadeDelecoes = Transacao.query.delete()

    return make_response(200)

@app.route("/teste", methods=["GET"])
def teste():
     tempoAtual = datetime.now()
     return make_response({"tempoAtual": tempoAtual.isoformat()}, 200)

@app.route("/estatistica", methods=["GET"])
def calcularEstatisticas():
    tempoAtual = datetime.now()
    intervalo = timedelta(seconds=60)

    # Armazeno o tempo atual - 60 segundos
    filtro_transacoes = tempoAtual - intervalo

    transacoes = Transacao.query.filter(Transacao.dataHora >= filtro_transacoes).all()
    valores = [t.valor for t in transacoes]

    if valores:
        resultado = {
            'count': len(valores),
            'sum': sum(valores),
            'avg': sum(valores) / len(valores),
            'min': min(valores),
            'max': max(valores),
        }
    else:
        resultado = {
            'count': 0,
            'sum': 0.0,
            'avg': 0.0,
            'min': 0.0,
            'max': 0.0
        }

    return make_response(resultado, 200)