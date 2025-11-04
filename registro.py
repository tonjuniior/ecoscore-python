import datetime
from storage import carregar_registros, salvar_registros
from config_score import PONTUACAO_ECOSCORE, CATEGORIAS
from utils import score 

def coletar_e_pontuar_habitos_diarios(usuario):
    """
    Apresenta o formulário, coleta as respostas, calcula a pontuação e salva o registro.
    """
    data_hoje = datetime.date.today().strftime("%Y-%m-%d")
    todos_registros = carregar_registros()

    
    registros_usuario = [r for r in todos_registros if r['nome_usuario'] == usuario]
    if any(r['data'] == data_hoje for r in registros_usuario):
        print(f"\n🚫 Você já preencheu o registro para a data {data_hoje}.")
        return

    print("\n" + "="*40)
    print(f"FORMULÁRIO ECOSCORE - {data_hoje}")
    print("Preencha seus hábitos de hoje para receber sua pontuação.")
    print("="*40)

    respostas_diarias = {}
    pontuacao_total = 0

    
    for categoria in CATEGORIAS:
        opcoes = PONTUACAO_ECOSCORE[categoria]
        opcoes_lista = list(opcoes.keys())
        
        print(f"\n[{categoria}]:")
        
        
        for i, opcao in enumerate(opcoes_lista):
            pontos = opcoes[opcao]
            print(f"  [{i+1}] {opcao} ({pontos:+d} pts)")
        
        
        while True:
            escolhas_str = input(f"Selecione uma ou mais opções para {categoria} (ex: 1,3). Digite 0 para pular: ")
            if escolhas_str.strip() == '0':
                break

            indices_selecionados = []
            opcoes_selecionadas = []
            pontos_categoria = 0
            valido = True

            for part in escolhas_str.split(','):
                try:
                    indice = int(part.strip()) - 1
                    if 0 <= indice < len(opcoes_lista):
                        opcoes_selecionadas.append(opcoes_lista[indice])
                        pontos_categoria += opcoes[opcoes_lista[indice]]
                    else:
                        raise ValueError
                except ValueError:
                    print(f"Opção '{part.strip()}' inválida. Tente novamente.")
                    valido = False
                    break
            
            if valido:
                respostas_diarias[categoria.lower()] = ";".join(opcoes_selecionadas)
                pontuacao_total += pontos_categoria
                print(f"  -> Seleções para {categoria}: {', '.join(opcoes_selecionadas)}. Pontos: {pontos_categoria:+d}.")
                break

    
    novo_registro = {
        "nome_usuario": usuario,
        "data": data_hoje,
        "pontuacao": pontuacao_total,
        **respostas_diarias  
    }
    
    todos_registros.append(novo_registro)
    salvar_registros(todos_registros)

    print("\n" + "#"*40)
    print(f"🎉 Registro de hoje salvo! Sua pontuação total foi: {pontuacao_total:+d} pontos.")
    print("#"*40)