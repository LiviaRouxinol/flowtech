from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator

class Cliente(CrudBase):
    primary_key = "cliente_id"
    table = "cliente"
    fields = [
        "nome",
        "telefone",
        "cnpj",
        "e_mail",
        "endereco"
    ]

    def __init__(self, nome, telefone, cnpj, e_mail, endereco, id=None):
        self.id = id
        self.nome = nome
        self.telefone = telefone
        self.cnpj = cnpj
        self.e_mail = e_mail
        self.endereco = endereco

    def validate(self):
        erros = [
            Validator.required(self.nome, "nome"),
            Validator.required(self.cnpj, "cnpj"),
            Validator.required(self.e_mail, "e_mail"),
        ]
        return [erro for erro in erros if erro]

    @classmethod
    def has_related_records(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
        
            sql = "SELECT COUNT(*) FROM cliente WHERE id = %s"
            cursor.execute(sql, (id,))
            total = cursor.fetchone()[0]
            return total == 0 # Retorna True se não achar o cliente
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def safe_delete(cls, id):
        cliente = cls.find_by_id(id)
        if not cliente:
            raise ValueError("Cliente não encontrado.")
        cls.delete(id)
