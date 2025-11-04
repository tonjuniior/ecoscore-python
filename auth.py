from storage import carregar_usuarios, salvar_usuarios, carregar_registros, salvar_registros

def cadastro_usuario(nome_usuario, senha):
    """
    Cadastra um novo usuário e o inicializa no sistema de registro.
    Retorna True em sucesso, False se o usuário já existir.
    """
    lista_usuarios = carregar_usuarios()
    
    if any(u['nome_usuario'] == nome_usuario for u in lista_usuarios):
        print(f"\nUsuário '{nome_usuario}' já existe. Tente outro nome.")
        return False
    
    
    novo_usuario = {'nome_usuario': nome_usuario, 'senha': senha}
    lista_usuarios.append(novo_usuario)
    salvar_usuarios(lista_usuarios)
    
    print(f"\n✅ Usuário '{nome_usuario}' cadastrado com sucesso!")
    
    return True

def login_usuario(nome_usuario, senha):
    """
    Verifica se o usuário e a senha estão corretos.
    Retorna o nome_usuario em sucesso, None em falha.
    """
    lista_usuarios = carregar_usuarios()
    usuario_encontrado = None
    
    
    for u in lista_usuarios:
        if u.get('nome_usuario') == nome_usuario:
            usuario_encontrado = u
            break
            
    if not usuario_encontrado:
        print("\n❌ Login falhou: Usuário não encontrado.")
        return None
        
   
    if usuario_encontrado['senha'] == senha:
        print(f"\nBem-vindo(a) de volta, {nome_usuario}!")
        return nome_usuario
    else:
        print("\n❌ Login falhou: Senha incorreta.")
        return None

