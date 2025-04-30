from datetime import datetime, timezone
from . import db
from sqlalchemy.sql import func

class Transacao(db.Model):
    __tablename__ = "Transacoes"
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Numeric(10,2))
    dataHora = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    @property
    def serialize(self):

        return {
            "valor": self.valor,
            "dataHora": self.dataHora
        }