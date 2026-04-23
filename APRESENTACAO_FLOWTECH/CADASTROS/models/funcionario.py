from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator

class Funcionario(CrudBase):
    table = "funcionario"
    primary_key = "funcionario_id"
    fields = [
        "nome",
        "cpf",
        "e_mail",
        "setor",
        "cargo",
        "salario",
        "turno",
        "senha",
        "telefone",
        "data_nascimento"
    ]

    def __init__(self, nome, cnpj, telefone, e_mail, endereco, id=None):
        self.id = id 
        self.nome = nome
        self.cpf = cpf
        self.e_mail = e_mail
        self.setor = setor
        self.cargo = cargo
        self.salario = salario
        self.turno = turno
        self.senha = senha
        self.telefone = telefone
        self.data_nascimento = data_nascimento

    def validate(self):
        erros = [
            Validator.required(self.nome, "nome"),
            Validator.required(self.cpf, "cpf"),
            Validator.required(self.e_mail, "e_mail"),
        ]
        return [erro for erro in erros if erro]

    @classmethod
    def has_related_records(cls, funcionario_id):
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
        
            sql = "SELECT COUNT(*) FROM funcionario WHERE funcionario_id = %s"
            cursor.execute(sql, (funcionario_id,))
            total = cursor.fetchone()[0]
            return total == 0 # Retorna True se não achar o funcionario
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def safe_delete(cls, funcionario_id):
        funcionario = cls.find_by_id(funcionario_id)
        if not funcionario:
            raise ValueError("funcionario não encontrado.")
        
        return super().delete(funcionario_id)
