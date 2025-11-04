from storage import carregar_registros, carregar_usuarios
from config_score import PONTUACAO_ECOSCORE, CATEGORIAS
from collections import defaultdict



DICAS = {
    "TRANSPORTE": "Se seu score em Transporte está baixo, que tal planejar uma 'Segunda de Carona' ou testar o transporte público? Cada viagem conta!",
    "RESIDUOS": "Separe seu lixo orgânico do reciclável. Se já recicla, o próximo passo é a compostagem! Isso melhora muito seu score.",
    "ENERGIA": "Verifique os 'vampiros de energia': retire carregadores da tomada quando não estiverem em uso e desligue o monitor do PC. Pequenos gestos, grandes pontos!",
    "ALIMENTACAO": "Reduza o consumo de carne vermelha. Tente incluir uma refeição vegetariana ou vegana por dia para um grande impacto no seu EcoScore."
}



def analisar_pior_categoria(historico):
    """
    Analisa o último registro para encontrar a categoria de pior pontuação no dia.
    Isso é usado para personalizar a dica.
    """
    if not historico:
        return None

    ultimo_registro = historico[-1] 
    pior_categoria = None
    pior_pontuacao = float('inf')

    
    for categoria_upper in CATEGORIAS:
        try:
            categoria_lower = categoria_upper.lower()
            respostas_str = ultimo_registro.get(categoria_lower)
            if not respostas_str: continue

            # Divide as respostas e calcula a pontuação total da categoria
            respostas = respostas_str.split(';')
            pontuacao_categoria = sum(PONTUACAO_ECOSCORE[categoria_upper].get(r, 0) for r in respostas)

            # Compara a pontuação total da categoria
            if pontuacao_categoria < pior_pontuacao:
                pior_pontuacao = pontuacao_categoria
                pior_categoria = categoria_upper
        except KeyError:
            
            continue

    return pior_categoria

def get_dados_desempenho(usuario):
    """
    Calcula os dados de desempenho para um usuário e retorna um dicionário.
    Ideal para uso em aplicações web.
    """
    todos_registros = carregar_registros()
    historico = [r for r in todos_registros if r.get('nome_usuario') == usuario]

    if not historico:
        return None

    
    historico_ordenado = sorted(historico, key=lambda r: r.get('data', ''))

    total_dias = len(historico_ordenado)
    pontuacao_total = sum(r['pontuacao'] for r in historico_ordenado)
    media_diaria = pontuacao_total / total_dias if total_dias > 0 else 0

    
    historico_grafico = historico_ordenado[-30:]
    chart_labels = [r.get('data', '') for r in historico_grafico]
    chart_data = [r.get('pontuacao', 0) for r in historico_grafico]

    # --- Cálculo para o gráfico de categorias ---
    category_totals = defaultdict(float)
    category_counts = defaultdict(int)
    
    mapa_chaves = {
        "TRANSPORTE": "transporte",
        "RESÍDUOS": "residuos",
        "ALIMENTAÇÃO": "alimentacao",
        "ENGAJAMENTO E MATERIAIS": "engajamento"
    }
    mapa_inverso = {v: k for k, v in mapa_chaves.items()}

    for registro in historico_ordenado:
        for chave_csv, categoria_upper in mapa_inverso.items():
            # Normaliza a busca de chaves, tratando casos com e sem acentos
            chave_no_registro = next((k for k in registro if k.lower() == chave_csv), None)
            
            if chave_no_registro and registro[chave_no_registro]:
                respostas = registro[chave_no_registro].split(';')
                score_do_dia = sum(PONTUACAO_ECOSCORE[categoria_upper].get(r, 0) for r in respostas)
                category_totals[categoria_upper] += score_do_dia
                category_counts[categoria_upper] += 1
    
    category_avg_scores = {
        cat.replace(' E ', '/').title(): category_totals[cat] / category_counts[cat] if category_counts[cat] > 0 else 0
        for cat in mapa_chaves.keys()
    }
    
    category_chart_labels = list(category_avg_scores.keys())
    category_chart_data = list(category_avg_scores.values())
    # --- Fim do cálculo ---

    return {
        'pontuacao_total': pontuacao_total,
        'media_diaria': media_diaria,
        'historico_recente': historico_ordenado[-5:],
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'category_chart_labels': category_chart_labels,
        'category_chart_data': category_chart_data
    }

def get_dica_personalizada(usuario):
    """
    Analisa o último registro do usuário e retorna uma dica personalizada em um dicionário.
    """
    todos_registros = carregar_registros()
    historico = [r for r in todos_registros if r.get('nome_usuario') == usuario]

    if not historico:
        return {
            'titulo': "Comece sua jornada!",
            'texto': "Você ainda não possui registros. Preencha o formulário de hábitos para começar a receber dicas personalizadas."
        }

    
    historico_ordenado = sorted(historico, key=lambda r: r.get('data', ''))
    ultimo_registro = historico_ordenado[-1]
    pior_categoria = analisar_pior_categoria(historico_ordenado)

    
    if pior_categoria:
        try:
            # Calcula a pontuação total da pior categoria para decidir se a dica é necessária
            respostas_str = ultimo_registro.get(pior_categoria.lower(), "")
            respostas = respostas_str.split(';')
            pontuacao_da_pior_categoria = sum(PONTUACAO_ECOSCORE[pior_categoria].get(r, 0) for r in respostas)

            if pontuacao_da_pior_categoria < 0:
                return {
                    'titulo': f"💡 Foco em: {pior_categoria.title()}",
                    'texto': DICAS.get(pior_categoria, "Continue se esforçando! Cada pequena ação conta.")
                }
        except KeyError:
            pass 

    
    return {
        'titulo': "✨ Parabéns!",
        'texto': "Seu último registro foi excelente! Continue com os bons hábitos. Um ótimo desafio é tentar manter essa performance por uma semana inteira."
    }

def exibir_desempenho(usuario):
    """Calcula e exibe a pontuação total, a média e o histórico recente do usuário."""

    todos_registros = carregar_registros()
    historico = [r for r in todos_registros if r['nome_usuario'] == usuario]

    if not historico:
        print("\nℹ️ Você ainda não possui registros. Preencha o formulário primeiro!")
        return

    total_dias = len(historico)
    pontuacao_total = sum(registro['pontuacao'] for registro in historico)

   
    media_diaria = pontuacao_total / total_dias if total_dias > 0 else 0

    print("\n" + "💰"*20)
    print(f"RESUMO DE DESEMPENHO DE {usuario.upper()}")
    print("💰"*20)
    print(f"Período Total Registrado: {total_dias} dias")
    print(f"Pontuação Total Acumulada: {pontuacao_total:+d} pontos")
    print(f"Média Diária (EcoScore): {media_diaria:.2f} pontos")

    print("\nÚLTIMOS REGISTROS (5 dias):")
    
    for i, registro in enumerate(historico[-5:]):
        print(f"  {i+1}. Data: {registro['data']} | Pontos: {registro['pontuacao']:+d}")

    
    return analisar_pior_categoria(historico)



def gerar_dicas(usuario):
    """Gera uma dica personalizada com base na categoria de pior desempenho recente."""

    
    pior_categoria = exibir_desempenho(usuario)

    if pior_categoria is None:
        return

    
    if pior_categoria is not None:
        try:
            
            todos_registros = carregar_registros()
            historico_usuario = [r for r in todos_registros if r['nome_usuario'] == usuario]
            ultimo_registro = historico_usuario[-1]
            
            respostas_str = ultimo_registro.get(pior_categoria.lower(), "")
            respostas = respostas_str.split(';')
            pontuacao_da_pior_categoria = sum(PONTUACAO_ECOSCORE[pior_categoria].get(r, 0) for r in respostas)
            
            if pontuacao_da_pior_categoria >= 0:
                 print("\n\n✨ Excelente trabalho! Seu último registro foi muito positivo. Aqui está um desafio:")
                 print("⭐ Tente manter todos os hábitos positivos por 7 dias seguidos!")
                 return
        except KeyError:
            pass 

    print("\n" + "💡"*10)
    print(f"SUGESTÃO DE MELHORIA - FOCO: {pior_categoria}")
    print("💡"*10)

    dica_personalizada = DICAS.get(pior_categoria, "Continue se esforçando! Seu progresso é importante para o planeta.")

    print(dica_personalizada)


    
def get_dados_analise_geral():
    """
    Calcula dados de análise global para todos os usuários e registros.
    """
    todos_registros = carregar_registros()
    todos_usuarios = carregar_usuarios()

    num_usuarios = len(todos_usuarios)
    num_registros = len(todos_registros)

    if num_registros == 0:
        return {
            'num_usuarios': num_usuarios,
            'num_registros': 0,
            'media_geral': 0,
            'ranking': [],
            'category_chart_labels': [],
            'category_chart_data': []
        }

    # Calcular ranking de usuários
    pontuacao_por_usuario = defaultdict(float)
    for r in todos_registros:
        pontuacao_por_usuario[r['nome_usuario']] += r['pontuacao']
    
    ranking = sorted(pontuacao_por_usuario.items(), key=lambda item: item[1], reverse=True)
    
    # Calcular média geral
    pontuacao_total_geral = sum(r['pontuacao'] for r in todos_registros)
    media_geral = pontuacao_total_geral / num_registros

    # Calcular média por categoria (global)
    category_totals = defaultdict(float)
    category_counts = defaultdict(int)
    
    mapa_chaves = {
        "TRANSPORTE": "transporte",
        "RESÍDUOS": "residuos",
        "ALIMENTAÇÃO": "alimentacao",
        "ENGAJAMENTO E MATERIAIS": "engajamento"
    }
    mapa_inverso = {v: k for k, v in mapa_chaves.items()}

    for registro in todos_registros:
        for chave_csv, categoria_upper in mapa_inverso.items():
            chave_no_registro = next((k for k in registro if k.lower() == chave_csv), None)
            
            if chave_no_registro and registro[chave_no_registro]:
                respostas = registro[chave_no_registro].split(';')
                score_do_dia = sum(PONTUACAO_ECOSCORE[categoria_upper].get(r, 0) for r in respostas)
                category_totals[categoria_upper] += score_do_dia
                category_counts[categoria_upper] += 1
    
    # Média por registro
    category_avg_scores = {
        cat.replace(' E ', '/').title(): category_totals[cat] / category_counts[cat] if category_counts[cat] > 0 else 0
        for cat in mapa_chaves.keys()
    }
    
    category_chart_labels = list(category_avg_scores.keys())
    category_chart_data = list(category_avg_scores.values())

    return {
        'num_usuarios': num_usuarios,
        'num_registros': num_registros,
        'media_geral': media_geral,
        'ranking': ranking[:10],  # Top 10
        'category_chart_labels': category_chart_labels,
        'category_chart_data': category_chart_data
    }