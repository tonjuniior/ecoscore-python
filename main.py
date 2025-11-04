from auth import cadastro_usuario, login_usuario
from registro import coletar_e_pontuar_habitos_diarios
from desempenho import exibir_desempenho, gerar_dicas 

def menu_logado(usuario):
    """Menu para o usuário após o login."""
    while True:
        print("\n" + "="*30)
        print(f"BEM-VINDO(A), {usuario.upper()}")
        print("="*30)
        print("[1] Preencher Hábitos de Hoje (EcoScore)")
        print("[2] Ver Meu Desempenho (Histórico e Total)")
        print("[3] Ver Dicas Sustentáveis Personalizadas")
        print("[4] Sair/Logout")
        
        escolha = input("Selecione uma opção: ")
        
        if escolha == '1':
            coletar_e_pontuar_habitos_diarios(usuario)
        elif escolha == '2':
            exibir_desempenho(usuario)
        elif escolha == '3':
            gerar_dicas(usuario)
        elif escolha == '4':
            print("\n👋 Você saiu do sistema. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")


def menu_principal():
    """Menu inicial para autenticação."""
    print("="*40)
    print("EcoScore: Monitoramento de Hábitos")
    print("="*40)
    
    usuario_logado = None
    
    while usuario_logado is None:
        print("\nMENU PRINCIPAL:")
        print("[1] Login")
        print("[2] Cadastro")
        print("[3] Sair do Programa")
        
        escolha = input("Selecione uma opção: ")
        
        if escolha == '1':
            nome = input("Usuário: ")
            senha = input("Senha: ")
            usuario_logado = login_usuario(nome, senha)
            
        elif escolha == '2':
            nome = input("Novo Usuário: ")
            senha = input("Nova Senha: ")
            cadastro_usuario(nome, senha)
            
        elif escolha == '3':
            print("\nEncerrando o EcoScore. Tchau!")
            break
            
        else:
            print("Opção inválida.")

    if usuario_logado:
        menu_logado(usuario_logado)


if __name__ == '__main__':
    menu_principal()