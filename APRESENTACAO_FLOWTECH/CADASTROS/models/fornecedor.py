from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator

class Fornecedor(CrudBase):
    table = "fornecedor"
    primary_key = "fornecedor_id"
    fields = [
        "nome",
        "cnpj",
        "telefone",
        "e_mail",
        "endereco"
    ]

    def __init__(self, nome, cnpj, telefone, e_mail, endereco, id=None):
        self.id = id 
        self.nome = nome
        self.cnpj = cnpj
        self.telefone = telefone
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
    def has_related_records(cls, fornecedor_id):
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
        
            sql = "SELECT COUNT(*) FROM fornecedor WHERE fornecedor_id = %s"
            cursor.execute(sql, (fornecedor_id,))
            total = cursor.fetchone()[0]
            return total == 0 # Retorna True se não achar o fornecedor
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def safe_delete(cls, fornecedor_id):
        fornecedor = cls.find_by_id(fornecedor_id)
        if not fornecedor:
            raise ValueError("Fornecedor não encontrado.")
        
        return super().delete(fornecedor_id)
