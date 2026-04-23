from core.database import Database

class CrudBase:
    table = ""
    fields = []
    primary_key = "id"  # Nome padrão da PK

    @classmethod
    def find_all(cls, order_by=None):
        # Se não passar ordem, usa a chave primária da classe
        order_field = order_by if order_by else cls.primary_key
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = f"SELECT * FROM {cls.table} ORDER BY {order_field}"
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def find_by_id(cls, id_value):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)
        try:
            sql = f"SELECT * FROM {cls.table} WHERE {cls.primary_key} = %s"
            cursor.execute(sql, (id_value,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def delete(cls, id_value):
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            # Garanta que está usando {cls.primary_key}
            sql = f"DELETE FROM {cls.table} WHERE {cls.primary_key} = %s"
            cursor.execute(sql, (id_value,))
            conexao.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conexao.close()


    def insert(self):
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            colunas = ", ".join(self.fields)
            marcadores = ", ".join(["%s"] * len(self.fields))
            # Pega os valores dos atributos listados em self.fields
            valores = tuple(getattr(self, campo) for campo in self.fields)
            sql = f"INSERT INTO {self.table} ({colunas}) VALUES ({marcadores})"
            cursor.execute(sql, valores)
            conexao.commit()
            return cursor.lastrowid
        except Exception:
            conexao.rollback()
            raise
        finally:
            cursor.close()
            conexao.close()

    def update(self, id_value):
        conexao = Database.connect()
        cursor = conexao.cursor()
        try:
            campos = ", ".join([f"{campo} = %s" for campo in self.fields])
            valores = tuple(getattr(self, campo) for campo in self.fields) + (id_value,)
            sql = f"UPDATE {self.table} SET {campos} WHERE {self.primary_key} = %s"
            cursor.execute(sql, valores)
            conexao.commit()
            return cursor.rowcount
        except Exception:
            conexao.rollback()
            raise
        finally:
            cursor.close()
            conexao.close()
