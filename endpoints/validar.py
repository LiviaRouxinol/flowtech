# ============================================================
# VALIDAR NOME
# ============================================================
def validar_nome(nome):
    if not nome or len(nome.strip()) < 3:
        return False
    if " " not in nome.strip():
        return False
    return True


# ============================================================
# VALIDAR TELEFONE
# ============================================================
def validar_tel(telefone):
    telefone = str(telefone)
    return telefone.isdigit() and len(telefone) == 11


# ============================================================
# VALIDAR SENHA
# ============================================================
def validar_senha(senha):
    if len(senha) < 8:
        return False
    if not any(c.isdigit() for c in senha):
        return False
    if not any(c.isupper() for c in senha):
        return False
    if not any(c.islower() for c in senha):
        return False
    return True


# ============================================================
# VALIDAÇÃO COMPLETA DO FUNCIONÁRIO
# ============================================================
def validacao_funcionario(dados):
    token = "SEU_TOKEN_AQUI"  # depois você substitui pelo seu

    if not validar_nome(dados.get("nome", "")):
        return {"status": "erro", "mensagem": "Nome inválido"}

    if not validar_email(dados.get("e_mail", ""), token):
        return {"status": "erro", "mensagem": "E-mail inválido"}

    if not validar_cpf(dados.get("CPF", ""), token):
        return {"status": "erro", "mensagem": "CPF inválido"}

    if not validar_tel(dados.get("telefone", "")):
        return {"status": "erro", "mensagem": "Telefone inválido"}

    if not validar_senha(dados.get("senha", "")):
        return {"status": "erro", "mensagem": "Senha inválida"}

    return {"status": "sucesso", "mensagem": "Validação concluída"}



import requests

# ============================================================
# VALIDAR EMAIL (API EXTERNA)
# ============================================================
def validar_email(email, token):
    url = "https://api.invertexto.com/v1/email-validator"
    params = {
        "token": token,
        "value": email
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        return data.get("valid", False)
    except:
        return False


# ============================================================
# VALIDAR CPF (API EXTERNA)
# ============================================================
def validar_cpf(cpf, token):
    url = "https://api.invertexto.com/v1/validator"
    params = {
        "token": token,
        "value": cpf
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        return data.get("valid", False)
    except:
        return False
